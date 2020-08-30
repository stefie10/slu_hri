from carmen_util import *
from Tkinter import *
import Image            #PIL
import ImageTk          #PIL
import sys
import getopt
from math import *
from random import randint 
from tkSimpleDialog import askstring
from tkFileDialog import askopenfilename, asksaveasfilename, askdirectory
#from pyTklib import *
from scipy.misc import toimage
from scipy import ones, transpose
from annote_utils import *
import glob
from cPickle import dump
from classifier_util import load_groundtruth_str
from xml_util import *
from os.path import exists
from os import mkdir

class ImageAnnoter:
    def __init__(self):
        self.root = Tk()
        self.photo = None
        self.photo2 = None


        self.topframe = Frame()
        self.topframe.pack(side=TOP, fill=X)

        b = Button(self.topframe, text="<", width=6, 
                   command=self.prev_image, justify=CENTER, anchor=N);
        b.pack(side=LEFT, padx=2, pady=2);

        b = Button(self.topframe, text=">", width=6,
                   command=self.next_image, justify=CENTER, anchor=N);
        b.pack(side=LEFT, padx=2, pady=2);




        self.canvas = Canvas(self.root,height=400,width=400)
        self.canvas.bind('<Button-1>', self.onmouseclick)
        self.canvas.bind_all('<Key>', self.allkey)
        self.canvas.pack(side=TOP,fill=BOTH,expand=0)
        
        
        self.sf = 2
        self.curr_image_index = 0
        self.image_filenames = []

        self.click1 = None
        self.click2 = None
        self.curr_objs = []
        self.height = None
        self.width = None
        self.dirname = None
        self.dirname_out = None
        self.prev_obj = "door"
        
        self.colors = ["red", "green", "yellow", "magenta", 
                       "purple", "orange", "brown", "tan", "pink"]

        self.run()


    def allkey(self, event):
        if event.keysym == 'Escape':
            try:
                self.curr_objs.pop()
                self.draw_image(False)
            except(IndexError):
                pass

    def onmouseclick(self, click):
        if(len(self.image_filenames) == 0):
            return
        
        myobj = {}

        if(self.click1 == None):
            self.click1 = [click.x, click.y]
        else:
            self.click2 = [click.x, click.y]
            print "******************"
            print self.click1
            print self.click2  
            
            dlg = MyDialog(self.prev_obj)
            dlg.transient(self.root)
            #dlg.grab_set()
            dlg.focus_set()
            self.root.wait_window(dlg)
            obj, orient, trunc, occ, diff =   dlg.get_result()

            myobj['name']=obj
            myobj['pose']=orient
            myobj['truncated']=trunc;
            myobj['occluded']=occ;
            myobj['difficult']=diff;
            myobj['bndbox']={'xmin':self.click1[0]*self.sf, 'ymin':self.click1[1]*self.sf,
                             'xmax':self.click2[0]*self.sf, 'ymax':self.click2[1]*self.sf}
            
            self.curr_objs.append(myobj)

            self.click1 = None
            self.click2 = None
            self.prev_obj = obj
            
        self.draw_image(False)


    def next_image(self):
        print self.image_filenames[self.curr_image_index]
        #save everything here
        if(self.curr_objs != [] and self.dirname_out != None):
            subannote = {}
            subannote["object"] = self.curr_objs
            subannote["folder"] = "tkollar_VOC"
            subannote["filename"] = self.image_filenames[self.curr_image_index].split("/")[-1]
            subannote["source"] = {"database":"Tom Kollar's Database", 
                                   "annotation":"Tom Kollar", 
                                   "image":"flickr", 
                                   "flickrid":"n/a"}

            subannote["owner"] = {"flickrid":"n/a", "name":"n/a"}
            subannote["size"] = {"width":self.width, 
                                 "height":self.height, 
                                 "depth":self.channels}
            subannote["segmented"] = 0;

            myannotation = {}
            myannotation["annotation"] = subannote
            
            xmlfilename = self.image_filenames[self.curr_image_index].split('/')[-1].replace('.jpg', '.xml')
            save_xml(myannotation, self.dirname_out+xmlfilename)
        

        self.curr_objs = []
        self.height = None
        self.width = None

        #plot the current image
        self.curr_image_index += 1
        print "curr image", self.curr_image_index
        self.draw_image()

    def prev_image(self):
        self.curr_image_index -= 1
        self.curr_objs = []
        self.height = None
        self.width = None
        self.draw_image()
    
    def draw_image(self, load_xml=True):
        self.canvas.delete(ALL)
        
        if(self.image_filenames == []):
            return

        print self.image_filenames[self.curr_image_index].split("/")[-1]
        im = Image.open(self.image_filenames[self.curr_image_index])
        im = im.resize([int(im.size[0])/self.sf, int(im.size[1])/self.sf])

        if(self.dirname_out != None and load_xml):
            xml_filename = self.image_filenames[self.curr_image_index].split('/')[-1].replace('.jpg', '.xml')
            if(exists(self.dirname_out+xml_filename)):
                self.load_xml(self.dirname_out+xml_filename)

        
        self.canvas.configure(width = im.size[0], height = im.size[1])
        self.photo2 = ImageTk.PhotoImage(im)
        item = self.canvas.create_image(0,im.size[1],anchor=SW,image=self.photo2)
        self.width = im.size[0]
        self.height = im.size[1]
        self.channels = len(im.getbands())

        for obj in self.curr_objs:
            x1, y1 = obj["bndbox"]["xmin"]/self.sf, obj["bndbox"]["ymin"]/self.sf
            x2, y2 = obj["bndbox"]["xmax"]/self.sf, obj["bndbox"]["ymax"]/self.sf
            self.canvas.create_rectangle((x1,y1,x2,y2), outline="red", width="3.0")
            self.canvas.create_rectangle((x1-30, y1-8, x1+30, y1+8), fill="white")
            self.canvas.create_text((x1, y1), text=obj["name"], activefill="red")

                                         
            
        
    def run(self):
        #add the menu items
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open Image Logfile", command=self.open_image_logfile)
        filemenu.add_command(label="Open XML (single image)", command=self.open_xml)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # display the menu
        self.root.config(menu=menubar)
        mainloop()


    def open_xml(self):
        xml_filename = askopenfilename()
        self.load_xml(xml_filename);
        self.draw_image()


    def load_xml(self, xml_filename):
        self.curr_objs = parse_xml(xml_filename)["annotation"]["object"]

        print "objects",self.curr_objs
        
        if(not isinstance(self.curr_objs, list)):
            self.curr_objs = [self.curr_objs]
        


        for elt in self.curr_objs:
            elt["bndbox"]["xmin"] = float(elt["bndbox"]["xmin"])
            elt["bndbox"]["ymin"] = float(elt["bndbox"]["ymin"])
            elt["bndbox"]["xmax"] = float(elt["bndbox"]["xmax"])
            elt["bndbox"]["ymax"] = float(elt["bndbox"]["ymax"])
            


            
    def open_image_logfile(self):
        self.curr_image_index = 0
        self.dirname = askdirectory()
        self.image_filenames = glob.glob(self.dirname + "/*.jpg")
        #self.image_filenames = glob.glob(self.dirname + "/*.jpeg")
        #dirname = askdirectory()

        if(len(self.image_filenames) == 0):
            self.image_filenames = glob.glob(self.dirname + "/*.jpeg")
        if(len(self.image_filenames) == 0):
            self.image_filenames = glob.glob(self.dirname + "/*.png")
        
        self.image_filenames.sort()


        self.dirname_out = ""
        spldir = self.dirname.split("/")[:-1]

        for elt in spldir:
            if(elt != ""):
                self.dirname_out += "/" + elt

        self.dirname_out += "/annotations/"
        
        print "out filename", self.dirname_out
        if(not exists(self.dirname_out)):
            mkdir(self.dirname_out)

        #self.next_image()
        self.draw_image()
        

class MyDialog(Toplevel):
    def __init__(self, default_obj="door"):
        Toplevel.__init__(self)
        self.__result = None

        self.object = StringVar(self)
        self.object.set(default_obj) # default value
        
        w = OptionMenu(self, self.object, "clock", "screen", "microwave", 
                       "railing", "stairs", "refrigerator", "soap dispenser", 
                       "urinal", "faucet", "sink", "door", "window", 
                       "person", "tvmonitor", "pottedplant", "sofa","chair", "bottle", "cat", "dog",
                       "bicycle", "bird", "boat", "bus", "aeroplane",
                       "car", "cow", "diningtable", "horse", "motorbike", "sheep", "train")
        w.pack()
        
        self.varT = IntVar()
        c1 = Checkbutton(self, text="is truncated",
                        variable=self.varT)
        c1.pack()

        self.varO = IntVar()
        c2 = Checkbutton(self, text="is occluded",
                        variable=self.varO)
        c2.pack()

        self.varD = IntVar()
        c3 = Checkbutton(self, text="is difficult",
                        variable=self.varD)
        c3.pack()

        self.listbox = Listbox(self)
        self.listbox.config(height=5)
        self.listbox.pack()

        self.orient_data = ["Unspecified", "Frontal", 
                            "Rear", "SideFaceLeft", "SideFaceRight"]

        for item in self.orient_data:
            self.listbox.insert(END, item)

        Button(self, command=self.validate, text=' OK ').pack(side=TOP)


    def validate(self):
        orient = self.orient_data[map(int, self.listbox.curselection())[0]]
        self.__result = [self.object.get(), orient, self.varT.get(), 
                         self.varO.get(), self.varD.get()]
        self.destroy()

    def get_result(self):
        return self.__result

if __name__=="__main__":
    ia = ImageAnnoter()

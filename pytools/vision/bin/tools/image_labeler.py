#from carmen_util import *
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
#from scipy.misc import toimage
#from scipy import ones, transpose
from annote_utils import *
import glob
from cPickle import dump
from classifier_util import load_groundtruth_str

    
class ImageAnnoter:
    def __init__(self):
        self.root = Tk() 
        self.photo = None
        self.photo2 = None

        
        self.canvas = Canvas(self.root,height=400,width=400)
        self.canvas.pack(side=TOP,fill=BOTH,expand=0)
        #self.canvas.bind("<Button-1>", self.mouse_cb)
        
        b = Button(self.root, text="Skip 10", width=6, command=self.next_ten_image, justify=CENTER, anchor=N);
        b.pack(side=RIGHT, padx=2, pady=2);

        b = Button(self.root, text=">", width=6, command=self.next_image, justify=CENTER, anchor=N);
        b.pack(side=RIGHT, padx=2, pady=2);

        b = Button(self.root, text="<", width=6, command=self.prev_image, justify=CENTER, anchor=N);
        b.pack(side=RIGHT, padx=2, pady=2);
        
        b = Button(self.root, text="enter", width=6, command=self.add_tags, justify=CENTER, anchor=N);
        b.pack(side=BOTTOM, padx=2, pady=2);

        self.t = Text(self.root, width=50, height=1)
        self.t.pack(side=BOTTOM, padx=2, pady=2)

        #print dir(self.t)
        #self.t.delete(1.0, END)
        #self.t.insert(END, "test")
        
        self.curr_image_index = 0
        self.classifications = {}
        self.image_filenames = []

        self.colors = ["red", "green", "yellow", "magenta", "purple", "orange", "brown", "tan", "pink"]

        self.run()

    def add_tags(self):
        mykey = self.image_filenames[self.curr_image_index].split("/")[-1]
        self.classifications[mykey] = self.t.get(1.0, END).strip()
        self.t.delete(1.0, END)
        self.next_image()


    def next_image(self):
        #plot the current image
        self.curr_image_index += 5
        print "curr image", self.curr_image_index
        self.draw_image()

    def next_ten_image(self):
        #plot the current image
        self.curr_image_index += 10
        self.draw_image()

    def prev_image(self):
        self.curr_image_index -= 5
        self.draw_image()
    
    def draw_image(self):
        if(self.image_filenames == []):
            return
        
        mykey = self.image_filenames[self.curr_image_index].split("/")[-1]
        mykey2 = "000"+mykey.replace(".png", ".jpg")
        if(self.classifications.has_key(mykey)):
            self.t.delete(1.0, END)
            self.t.insert(END, str(self.classifications[mykey]).strip())
        elif(self.classifications.has_key(mykey2)):
            self.t.delete(1.0, END)
            self.t.insert(END, str(self.classifications[mykey2]).strip())

        im = Image.open(self.image_filenames[self.curr_image_index])
        im = im.resize([int(im.size[0]/2.0), int(im.size[1]/2.0)])
        
        self.canvas.configure(width = im.size[0], height = im.size[1])
        self.photo2 = ImageTk.PhotoImage(im)
        item = self.canvas.create_image(0,im.size[1],anchor=SW,image=self.photo2)
        
        
    def run(self):
        #add the menu items
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open Image Logfile", command=self.open_image_logfile)
        filemenu.add_command(label="Open Groundtruth", command=self.open_groundtruth_file)
        filemenu.add_command(label="Save Image Tags", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # display the menu
        self.root.config(menu=menubar)
        mainloop()

    def open_groundtruth_file(self):
        filename = askopenfilename() 
        curr_classifications = load_groundtruth_str(filename)
        
        self.classifications = {}
        for mykey in curr_classifications.keys():
            mystr = ""
            for val in curr_classifications[mykey]:
                mystr += str(val)+","
            self.classifications[mykey] = mystr


    def open_image_logfile(self):
        dirname = askdirectory()        
        self.image_filenames = glob.glob(dirname + "/*.jpg")

        if(len(self.image_filenames) == 0):
            self.image_filenames = glob.glob(dirname + "/*.png")
        
        self.image_filenames.sort()
        

    def save_file(self):
        filename = asksaveasfilename()
        print "saving file"
        dump(self.classifications, open(filename+".pck", 'w'))

        myfile = open(filename+".txt",  'w')

        print self.classifications
        for elt in self.classifications.keys():
            #val = elt.split("/")[-1];
            myfile.write(elt + ", ")
            myfile.write(self.classifications[elt])
            myfile.write("\n");

        myfile.close()

if __name__=="__main__":
    ia = ImageAnnoter()

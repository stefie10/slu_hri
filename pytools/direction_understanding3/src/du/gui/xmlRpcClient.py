import xmlrpclib
import time
import random


def main():
    print "hello"
    #proxy = xmlrpclib.ServerProxy("http://localhost:4243/du")


    commands = ["Walk to the kitchen.",
                "Walk to the sink in the kitchen.",
                "Walk to the kitchen and then go to the bathroom.",
                "Walk to the fireplace in the living room.",
                "Go to the living room by the fireplace.  Then walk into the dining room.  Finish by going to the kitchen.",
                "Fly down.",
                "Face the window.",
                "Fly up."
                ]

    while True:
        try:
            proxy = xmlrpclib.ServerProxy("http://quato:4243/du")
            command = random.choice(commands)
            print "sending", command
            proxy.du.sendCommand(command)
        except:
            pass
        

        time.sleep(25)
        

    
    
if __name__=="__main__":
    main()

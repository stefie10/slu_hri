import jpype
from environ_vars import TKLIB_HOME
import os

started = False

def startJvm():
    """
    Start the JVM.  There can only be one JVM per python instance.  So
    you have to write and call your own version of this method if you
    want to set the class path, etc.
    """
    global started

    if not started:
        import os
        print "loaded jvm", jpype.getDefaultJVMPath()
        classpath = ":".join([os.environ["CLASSPATH"]])
        print "classpath:", classpath
        jpype.startJVM(jpype.getDefaultJVMPath(),
                       "-ea",
                       "-Xms500m",
                       "-Xmx500m",
#                       "-Xrs",
#                       "-Xcheck:jni",
#                       "-Xcheck:nabounds",
#                       "-Djava.compiler=None",
                       "-Djava.class.path=%s" % classpath)
        
        started = True

startJvm()
                  

                   

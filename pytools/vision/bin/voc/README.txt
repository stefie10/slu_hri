For linux and python version 2.5 or greater, make sure that you have:

--------------------------------
To install:

1)  Check out the following utilities:
>> svn co https://svn.csail.mit.edu/rrg/tklib/utilities/

2) Put this in your python path:
>> export PYTHONPATH=$PYTHONPATH:PATH_TO_UTILITIES

3) Make sure you have the requisite packages:
>> apt-get install python-tk python-imaging python-imaging-tk python-scipy

4) Get the image labeller:

>> svn co https://svn.csail.mit.edu/rrg/tklib/pytools/vision/bin/voc/


---------------------------------
To run:

>> python image_labeler.py

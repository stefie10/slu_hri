###########gmapping######################
Website:
http://www.openslam.org/gmapping.html

Wiki page:
https://groups.csail.mit.edu/rvsn/wiki/index.php?title=WTBH:Gmapper_wheelchair

To use gmapping:

If you are using a hukuyo (I assume UTM) the gmapper code will not work out of the box (atleast if you want to convert the stuff back to a carmen log file) as it doesnt have the configuration settings for the hokuyo).  The above link describes the small modification that you need to do to get the correct type of log file from carmen.

Use the config file when you are using gfs_simplegui command

./gfs_simplegui -cfg config_file.txt -filename test outfilename map.gfs

Once the map (which is .gfs file whihc has the corrected laser and odometry data) is made by gmapper then you can convert it to back to carmen log file and use it to make a grid map if thats what you need.

./gfs2log map.gfs map.log

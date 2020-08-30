
CFLAGS = -c -pipe -Wall -W   -DQT_SHARED -DQT_NO_DEBUG -DQT_THREAD_SUPPORT  -fPIC -fpic
CFLAGS += -g
#CFLAGS += -O3



IFLAGS += -I. -I/usr/include/$(PYTHON)  -I../../build/include
CARMEN_IFLAGS = -I../../nlp/3rdParty/carmen/carmen/include 
QT_LFLAGS = -lqt-mt -lz -L/usr/X11R6/lib/libXext.so /usr/lib/libX11.so 
CARMEN_LFLAGS = -L../../nlp/3rdParty/carmen/carmen/lib/  -L../../build/lib -lspatial_features -lgsl_utilities

carmen: libtklib_utilities.a

clean:
	-rm *.o ../lib/*.a

libtklib_utilities.a: procrustes.o nearest_neighbor.o quaternion.o kmeans.o probability.o gaussian.o line.o box_window.o hurdle_extractor.o gsl_python.o EKF2D.o carmen_util.o gridmapping.o simulator.o noise_models.o spline.o carmen_subscribe.o carmen_publish.o tklib_log_gridmap.o 
	@echo Compiling libtklib_utilities.a
	ar cr ../lib/libtklib_utilities.a *.o

%.o: %.c
	g++ $(CFLAGS) $(CARMEN_IFLAGS) $(IFLAGS) $(LFLAGS) $(CARMEN_LFLAGS) -L../../3rdParty/libpolygon_2.0.3/lib/ -o $@ -c $<  


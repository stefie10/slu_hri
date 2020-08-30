all: build-swig
CFLAGS=`python-config --cflags` -Isrc 


build-swig: swig/math2d.i 
	swig -Isrc -Wall -python $<
	gcc -fPIC -o src/math2d.o -c src/math2d.c $(CFLAGS)
	gcc -fPIC -o swig/math2d_wrap.o -c swig/math2d_wrap.c $(CFLAGS)
	gcc -fPIC -o swig/_cMath2d.so swig/math2d_wrap.o src/math2d.o  -shared



clean:
	-@cd src && rm *.o
	-@cd swig && rm *.o
	-@rm swig/_cMath2d.so swig/*_wrap.c

//#include "quat2ang.h"
#include <carmen/carmen.h>
#include "quat2ang.h"



int main(int argc, char** argv){

  if(argc == 5){
    float a1 = atof(argv[1]);
    float a2 = atof(argv[2]);
    float a3 = atof(argv[3]);
    float a4 = atof(argv[4]);


    fprintf(stderr, "a1: %f, a2:%f, a3:%f, a4:%f\n", a1,a2,a3,a4);

    bduVec3f vec;
    bduVec4f temp;
    temp.n[0] = a1; temp.n[1] = a2; temp.n[2] = a3; temp.n[3] =a4;
    quat2ang(&temp, &vec);

    fprintf(stderr, "r: %f, p:%f, y:%f\n", vec.n[0], vec.n[1], vec.n[2]);
  }
  else
    fprintf(stderr, "usage: ./quat2ang a1 a2 a3 a4\n");
}

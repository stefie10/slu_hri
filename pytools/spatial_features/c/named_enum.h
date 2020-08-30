/*
* This file makes a named enum in in C with the preprocessor.
* To use it, #define the following variables, and then include this file:

* NAMED_ENUM_LIST - A comma separated list of the feature names,
* surrounded by a call to the "X" macro.
* NAMED_ENUM_FEATURE_INDEXES_NAME - the name of the enum that will be created, 
* containing the names defined above.
* NAMED_ENUM_CHAR_LIST_NAME - the name of the static char** array
* that will contain the names of the features as strings, in the same
* order as the enum.
* NAMED_ENUM_COUNT_NAME - the name of the variable that will contain
* the number of features.  This is defined as the last element of the enum.
*
* Here is an example: 
* #define NAMED_ENUM_LIST                              \
*   X(F_distFigureStartToGroundCentroid),               \
*    X(F_distFigureCenterOfMassToGroundCentroid),       \
*    X(F_distFigureEndToGroundCentroid),               \
*    X(F_distFigureStartToGround),                     \
*    X(F_distFigureEndToGround),                       \
*    X(F_averageDistStartEndGround),                   \
*    X(F_distFigureCenterOfMassToGround)
*#define NAMED_ENUM_FEATURE_INDEXES_NAME()  distance_path_to_landmark_fi
*#define NAMED_ENUM_CHAR_LIST_NAME()  distance_path_to_landmark_names
*#define NAMED_ENUM_COUNT_NAME()  distance_path_to_landmark_count
*#include "named_enum.h"
*/


#define X(x) x

enum NAMED_ENUM_FEATURE_INDEXES_NAME()
  {                                                     
    NAMED_ENUM_LIST,
    NAMED_ENUM_COUNT_NAME()
  };

#undef X

#define X(x) #x   


const static char * NAMED_ENUM_CHAR_LIST_NAME() [] =         
{                                                       

  NAMED_ENUM_LIST,
};                                                      

#undef X 

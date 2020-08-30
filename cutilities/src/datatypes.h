#ifndef DATATYPES_H
#define DATATYPES_H
typedef struct {
  double m;
  double b;
} tklib_line_t;

typedef struct {
  gsl_vector x_st[2];
  gsl_vector x_end[2];
  double dw;
  double height;
  
  tklib_line width_line;
  tklib_line height_line;

} tklib_box_window_t;

#endif

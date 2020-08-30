#ifndef TKLIB_LOCALIZE_H
#define TKLIB_LOCALIZE_H
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_block_float.h>
#include "gsl_utilities.h"
#include "probability.h"
#include "gsl_utilities.h"
#include "carmen_util.h"
#include "procrustes.h"
#include "noise_models.h"
#include "spline.h"
#include "carmen_publish.h"
#include "tklib_gridmap.h"
#include <carmen/localizecore.h>
#include <carmen/localize_motion.h>


#ifdef __cplusplus
extern "C" {
#endif

class tklib_localize{
 private:
  //variables
  tklib_gridmap gridmap;
  carmen_localize_particle_filter_p filter;
  carmen_localize_param_p filter_params;
  
 public:

  carmen_localize_param_p get_default_parameters();
  void update(gsl_vector* robot_pose, 
	      gsl_vector* readings, 
	      double offset, int backwards);
  tklib_localize();
  ~tklib_localize();
};


#ifdef __cplusplus
}
#endif


#endif

#ifndef BINARY_INFERENCE_H
#define BINARY_INFERENCE_H
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>
#include "gsl_utilities.h"
/*#include <gsl/gsl_block_float.h>
#include <gsl/gsl_math.h>
//#include "gsl_utilities.h"
#include "probability.h"

#include "carmen_util.h"
//#include "procrustes.h"
//#include "noise_models.h"
#include "spline.h"
#include "carmen_publish.h"*/


#ifdef __cplusplus
extern "C" {
#endif

class binary_node;
class binary_factor;

class binary_node{
 public:
  char* name;
  int mynumber;
  int num_entries;
  gsl_vector* connections;
  gsl_matrix* ntof_messages;
  gsl_matrix* fton_messages;

  binary_node(char* myname, int nodenumber, gsl_vector* myconnections);
  gsl_vector* marginal(void);
  void compute_ntof_messages(binary_factor* fnodes);
  gsl_vector* get_ntof_message(int nodenum);
};



class binary_factor{
  char* name;
  int mynumber;
  int num_entries;
  gsl_vector* connections;
  gsl_matrix* CPD;
  gsl_matrix* ntof_messages;
  gsl_matrix* fton_messages;
  gsl_matrix* configurations;
 
 public:
  binary_factor(char* myname, int nodenumber, 
		gsl_vector* myconnections, gsl_matrix* myCPD);
  void initialize_messages(void);
  void compute_fton_messages(binary_node* nodes);
  gsl_vector* get_fton_message(int nodenumber);
  double evaluate_configuration(gsl_vector* conf, int k);
  gsl_matrix* compute_configurations(gsl_vector* vars);
 private:
  gsl_vector* get_configuration_index(gsl_vector* conf, int k);
};



class binary_inference{
 public:
  //variables
  int bpIterations;
  bool bp_done;
  
  //constructor
  binary_inference(int iterations){
    bpIterations=iterations; 
    bp_done = false;
    //self.nodes = {}
    //self.fnodes = {}
  }
  ~binary_inference();
  
  void addNode(binary_node* node);
  gsl_vector* marginal(binary_node* hnode);
  void initializeMessages(void);
  void run_belief_propagation(void);
};

#ifdef __cplusplus
}
#endif


#endif

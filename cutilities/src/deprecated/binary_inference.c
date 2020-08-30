#include "binary_inference.h"

binary_node::binary_node(char* myname, int nodenumber,
			 gsl_vector* myconnections){

  //make this a binary node
  num_entries = 2;
  //set the name
  name = myname;
  mynumber = nodenumber;

  //add connections
  connections = myconnections;
  
  //initialize the node to factor messages
  ntof_messages = gsl_matrix_calloc(num_entries, connections->size);
  gsl_matrix_add_constant(ntof_messages, 1.0);

  //initialize the factor to node messages
  fton_messages = gsl_matrix_calloc(num_entries, connections->size);
  gsl_matrix_add_constant(fton_messages, 1.0);
}


gsl_vector* binary_node::marginal(void){
  //def marginal(self):
  gsl_vector* mvals = tklib_matrix_prod(fton_messages, 1);
  double Z = tklib_vector_sum(mvals);
  
  gsl_vector_scale(mvals, 1.0/(Z*1.0));
  return mvals;
}


binary_factor::binary_factor(char* myname, 
			     int nodenumber,
			     gsl_vector* myconnections, 
			     gsl_matrix* myCPD){
  num_entries = 2;
  //set the name
  name = myname;
  mynumber = nodenumber;

  //add connections
  connections = myconnections;
  CPD = myCPD;
  
  //initialize the node to factor messages
  ntof_messages = gsl_matrix_calloc(num_entries, connections->size);
  gsl_matrix_add_constant(ntof_messages, 1.0);
  
  //initialize the factor to node messages
  fton_messages = gsl_matrix_calloc(num_entries, connections->size);
  gsl_matrix_add_constant(fton_messages, 1.0);  

  configurations = compute_configurations(connections);
}

gsl_matrix* binary_factor::compute_configurations(gsl_vector* vars){
  vars = vars;
  return NULL;

  /*if(vars->size == 1){
    gsl_matrix* retmat = gsl_matrix_calloc(1, num_entries);
    size_t i;
    for(i = 0; i< (size_t)num_entries; i++){
      gsl_matrix_set(retmat, 0, i, i);
    }
    
    return retmat;
  }
  
  //get a view of the vector
  gsl_vector_view v = gsl_vector_subvector(vars, 1, vars->size);
  gsl_matrix* result = compute_configurations(&v.vector);
  
  //get the new matrix
  gsl_matrix* fin_elts = gsl_matrix_calloc(num_entries, result->size2*num_entries);
  
  size_t i; size_t j;
  for(i=0; i<(size_t)num_entries; i++){
    for(j=0; j<result->size2; j++){
      gsl_vector_view myv = gsl_matrix_column(result, j);
      gsl_vector_view myv2 = gsl_matrix_subcolumn(fin_elts, 
						  j+i*result->size2, 
						  1, fin_elts->size1);
      
      //copy myv2 to myv
      gsl_vector_memcpy(&myv2.vector, &myv.vector);
      gsl_matrix_set(fin_elts, 0, j+i*result->size2, i);
    }
  }

  gsl_matrix_free(result);
  return fin_elts;
  */
}

gsl_vector* binary_factor::get_configuration_index(gsl_vector* conf, int k){
  gsl_vector* I = gsl_vector_calloc(conf->size-1);
  
  size_t i;
  size_t j=0;
  for(i = 0; i<conf->size;i++){
    if(j == (size_t)k){
      continue;
    }
    gsl_vector_set(I, j, i);
    j+=1;
  }

  return I;
}

double binary_factor::evaluate_configuration(gsl_vector* conf, int k){
  //get the configuration without k
  gsl_vector* I = get_configuration_index(conf, k);

  //take the elements associated with that configuration
  gsl_vector* newconf = tklib_vector_get(conf, I);

  //get the values of the associated messages
  gsl_vector* retvec = tklib_matrix_get_vector(ntof_messages, newconf, I);

  //take the product over this configuration
  double result = tklib_vector_prod(retvec);
  
  gsl_vector_free(newconf);
  gsl_vector_free(retvec);
  gsl_vector_free(I);
  
  return result;
}


void binary_factor::compute_fton_messages(binary_node*  nodes){

  //fton_messages = gsl_matrix_calloc();
  //self.fton_messages = get_mpf_matrix(2, len(self.connections), 0.0);
  
  gsl_matrix_set_all(fton_messages, 0.0);
  
  if(connections->size == 1){
    gsl_matrix_memcpy(fton_messages, CPD);
  }
  //gsl_vector_view v = gsl_matrix_column(fton_messages, 0);
  //fton_messages[:,0] = self.CPD


  //#copy over the current messages from the nodes to this factor
  nodes = nodes;
  /*size_t i;
  for(i=0; i<connections->size;i++){
    //stopped here
    self.ntof_vals[:,i] = nodes[nname].get_ntof_message(self.name);
    i+=1;
  }

  //#precompute all of the configurations
  for k in range(len(self.connections)){
      for i in range(len(self.configurations)){
	  myeval = self.evaluate_configuration(self.configurations[i], k);
	  
	  if(self.configurations[i][k] == 0){
	    self.fton_messages[0,k] += myeval*self.CPD[self.configurations[i][0],
						       self.configurations[i][1]];
	  }
	  else{
	    self.fton_messages[1,k] += myeval*self.CPD[self.configurations[i][0],
						       self.configurations[i][1]];
	  }
	}
	}*/
}

/*class BinaryFactor:

    def compute_fton_messages(self, nodes):
        self.fton_messages = get_mpf_matrix(2, len(self.connections), 0.0)

        if(len(self.connections) == 1):
            #print "fton:", self.name, " to ", self.connections
            #print self.CPD
            self.fton_messages[:,0] = self.CPD
            return

        #copy over the current messages from the nodes to this factor
        i = 0
        for nname in self.connections:
            self.ntof_vals[:,i] = nodes[nname].get_ntof_message(self.name)
            i+=1

        #precompute all of the configurations
        for k in range(len(self.connections)):
            for i in range(len(self.configurations)):
                myeval = self.evaluate_configuration(self.configurations[i], k)

                if(self.configurations[i][k] == 0):
                    self.fton_messages[0,k] += myeval*self.CPD[self.configurations[i][0],
                                                               self.configurations[i][1]]
                else:
                    self.fton_messages[1,k] += myeval*self.CPD[self.configurations[i][0],
                                                               self.configurations[i][1]]
        #print "fton:", self.name, " to ", self.connections
        #for i in range(len(self.fton_messages[0])):
        #    print self.fton_messages[:,i]
        #raw_input()
   
    def get_fton_message(self, nodename):
        i = self.connection_hash[nodename]
        return self.fton_messages[:,i]
*/

void binary_node::compute_ntof_messages(binary_factor* fnodes){
  //first, fill up all the current fton messages
  
  size_t i;
  for(i=0; i < connections->size; i++){
    // in self.connections{
    binary_factor fnode = fnodes[(int)gsl_vector_get(connections, i)];
    
    //get the message from the factor node to this node
    gsl_vector* my_message = fnode.get_fton_message(mynumber);

    //set my version of this message from the factor node to this node
    gsl_matrix_set_col(fton_messages, i, my_message);
  }
 
  //then compute the new values
  gsl_matrix* result = gsl_matrix_calloc(num_entries, connections->size);
  gsl_matrix_set_all(result, 1.0);

  //prod_msg = get_mpf_matrix(2, len(self.connections), 


  gsl_vector* prod_msg = tklib_matrix_prod(fton_messages, 1);
  tklib_matrix_mul_vec_inplace(result, prod_msg);
  

  gsl_matrix_add_constant(fton_messages, 0.00000000000000000000000000000000000000001);
  gsl_matrix_div_elements(result, fton_messages);
  gsl_matrix_memcpy(ntof_messages, result);

  gsl_vector_free(prod_msg);
  gsl_matrix_free(result);
}

gsl_vector* binary_node::get_ntof_message(int nodenum){
  size_t i;
  gsl_vector* ret_msg = gsl_vector_calloc(num_entries);
  
  for(i=0; i < connections->size; i++){
    if(gsl_vector_get(connections, i) == nodenum){
      printf("getting message\n");
      gsl_matrix_get_col(ret_msg, ntof_messages, i);
    }
  }
  
  return ret_msg;
}


/*class BinaryInference:

    #type can be "BP" or "Exact"
    def __init__(self, iterations=100):
        #each of these is hashed on the node name
        #it is assumed that no two node names are the same
        self.bpIterations = iterations
        self.bp_done = False
        self.nodes = {}
        self.fnodes = {}

    def addNode(self, node):
        #if there is already a name in the list
        #then don't add this node
        #print node.name
        if(node.name in self.nodes.keys() 
           or node.name in self.fnodes.keys()):
            print "Variable already defined"
            sys.exit(0)
            
        #add these nodes to the graph
        #only minimal checking is here right now...
        #for all I know, I don't even have a graph
        if(isinstance(node, BinaryFactor)):
            fnode = node
            
            #add connections to each node
            for myname in fnode.connections:
                #print "connection:", myname
                self.nodes[myname].add_connection(fnode.name)

            self.fnodes[fnode.name] = fnode

        elif(isinstance(node, BinaryNode)):
            #add the node name to the list of them
            self.nodes[node.name] = node
        else:
            print "Error, neither Factor nor Node"
            sys.exit(0)

    #for belief propagation this will only support 1 node in the list
    def marginal(self, hnode):
        if(not self.bp_done):
            self.run_belief_propagation()
            #print "just run bp"

        return hnode.marginal()

    def initializeMessages(self):
        for nodename in self.nodes.keys():
            self.nodes[nodename].initialize_messages()
        for fnode in self.fnodes.keys():
            self.fnodes[fnode].initialize_messages()

    def run_belief_propagation(self):
        print "initializing messages"
        self.initializeMessages()
        
        i = 0
        while(not self.bp_done):
            print "*************iteration*************" + str(i)

            #print "ntof messages"
            #t1 = clock()
            #pass some messages
            for node in self.nodes.keys():
                self.nodes[node].compute_ntof_messages(self.fnodes)
            #t2 = clock()
                
            #print "fton messages"
            for fnode in self.fnodes.keys():
                self.fnodes[fnode].compute_fton_messages(self.nodes) 

            #t3 = clock()
            #print "t ntof=", t2-t1
            #print "t fton=", t3-t2
            
            #if we've completed our bp iterations, then stop
            if(i > self.bpIterations):
                self.bp_done = True
            i=i+1
            #raw_input()

            
    def retMPF(self, initVal):
        return mpf(initVal)

    def makeMPFarray(self, size, initVal=1.0):
        tmp=[]
        for i in range(size):
            tmp.append(self.retMPF(initVal))        
        return tmp
*/

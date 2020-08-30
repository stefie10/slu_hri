/*********************************************************
 *
 * This source code is part of the Carnegie Mellon Robot
 * Navigation Toolkit (CARMEN)
 *
 * CARMEN Copyright (c) 2002 Michael Montemerlo, Nicholas
 * Roy, Sebastian Thrun, Dirk Haehnel, Cyrill Stachniss,
 * and Jared Glover
 *
 * CARMEN is free software; you can redistribute it and/or 
 * modify it under the terms of the GNU General Public 
 * License as published by the Free Software Foundation; 
 * either version 2 of the License, or (at your option)
 * any later version.
 *
 * CARMEN is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied 
 * warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
 * PURPOSE.  See the GNU General Public License for more 
 * details.
 *
 * You should have received a copy of the GNU General 
 * Public License along with CARMEN; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place, 
 * Suite 330, Boston, MA  02111-1307 USA
 *
 ********************************************************/


#include "global.h"

#define        NUM_ROBOT_NAMES        7

static carmen_default_message static_message = {0, 0};

static char *robot_names[] =
{"flo", "pearl", "robin", "dorothy", "oscar", "xavier", "walker"};

#define SP_SIZE 100
static char *search_path[SP_SIZE];
static int sp_num = 0;
#define RSP_SIZE 7
static const char *relative_search_path[RSP_SIZE] =
{"src", "include", "include/carmen", "bin", "lib", "doc", "man"};
static int rsp_num = RSP_SIZE;

typedef struct {
  char robot[200];
  char lvalue[200];
  char rvalue[200];
} ini_param;

#define MAX_PARAM_NUM 100
static ini_param param_list[MAX_PARAM_NUM];
static int param_num = 0;

static int carmen_carp_verbose;

int 
carmen_find_param(const char *lvalue)
{
  int i;
  
  for(i = param_num; i >= 0; i--)
    if(strcmp(param_list[i].lvalue, lvalue) == 0)
      return 1;
  return 0;
}

char *
carmen_param_pair(const char *lvalue)
{
  int i;

  for(i = param_num - 1; i >= 0; i--)
    if(strcmp(param_list[i].lvalue, lvalue) == 0) {
      if(strcmp(param_list[i].robot, "commandline") == 0 &&
	 strlen(param_list[i].rvalue) == 0)
	return NULL;
      else
	{
	  return param_list[i].rvalue;
	}
    }
  return NULL;
}

char *
carmen_param_pair_and_remove(const char *lvalue)
{
  int i, j;
  char *value;

  for(i = param_num - 1; i >= 0; i--)
    if(strcmp(param_list[i].lvalue, lvalue) == 0) {
      if(strcmp(param_list[i].robot, "commandline") == 0 &&
	 strlen(param_list[i].rvalue) == 0)
	return NULL;
      else
	{
	  value = (char *)calloc(strlen(param_list[i].rvalue)+1, sizeof(char));
	  carmen_test_alloc(value);

	  strcpy(value, param_list[i].rvalue);

	  for (j = i; j < param_num-1; j++)
	    { 
	      strcpy(param_list[j].robot, param_list[j+1].robot);
	      strcpy(param_list[j].lvalue, param_list[j+1].lvalue);
	      strcpy(param_list[j].rvalue, param_list[j+1].rvalue);
	    }
	  param_num--;

	  return value;
	}
    }
  return NULL;
}

int 
carmen_find_param_pair(const char *lvalue)
{
  if(carmen_find_param(lvalue) && 
     carmen_param_pair(lvalue) != NULL)
    return 1;
  else
    return 0;
}

int 
carmen_num_params(void)
{
  return param_num;
}

char *
carmen_get_param_by_num(int param_index)
{
  return param_list[param_index].lvalue;
}

int 
carmen_process_param_int(char *lvalue, carmen_usage_func usage, int *return_value) 
{
  char *endptr;
  char *arg;

  if(carmen_find_param(lvalue) > 0) 
    {
      if (carmen_find_param_pair(lvalue) == 0) 
	{
	  if(usage != NULL)
	    usage("Option '%s' requires argument: should be an integer.\n", 
		  lvalue);
	  // In case the user provided a usage that doesn't exit.
	  exit(-1);
	}
      arg = carmen_param_pair(lvalue);
      *return_value = strtol(arg, &endptr, 0);
      if (endptr == arg) 
	{
	  if(usage != NULL)
	    usage("Bad argument to int: %s, should be an integer.\n", arg);
	  // In case the user provided a usage that doesn't exit.
	  exit(-1);
	}
      return 1;
    }
  return 0;
}

double 
carmen_process_param_double(char *lvalue, carmen_usage_func usage, double *return_value) 
{
  char *endptr;
  char *arg;

  if (carmen_find_param(lvalue) > 0) 
    {
      if (carmen_find_param_pair(lvalue) == 0) 
	{
	  if(usage != NULL)
	    usage("Option '%s' requires argument: should be a double.\n", 
		  lvalue);
	  // In case the user provided a usage that doesn't exit.
	  exit(-1);
	}
      arg = carmen_param_pair(lvalue);
      *return_value = (double)strtod(arg, &endptr);
      if (endptr == arg) 
	{
	  if(usage != NULL)
	    usage("Bad argument to %s: %s, should be a double.\n", 
		  lvalue, arg);
	  // In case the user provided a usage that doesn't exit.
	  exit(-1);
	}
      return 1;
    }
  return 0;
}

int 
carmen_process_param_onoff(char *lvalue, carmen_usage_func usage, int *return_value) 
{
  char *arg;

  if (carmen_find_param(lvalue) > 0) 
    {
      if (carmen_find_param_pair(lvalue) == 0)
	{
	  usage("Option '%s' requires argument: should be on/off.\n", lvalue);
	  // In case the user provided a usage that doesn't exit.
	  exit(-1);
	}
      arg = carmen_param_pair(lvalue);
      if (strcmp(arg, "on") == 0)
	*return_value = 1;
      else if (strcmp(arg, "off") == 0)
	*return_value = 0;
      else
	usage("Bad argument to %s: %s, should be on/off.\n", lvalue, arg);
      return 1;
    }
  return 0;
}

char *
carmen_process_param_string(char *lvalue, carmen_usage_func usage) 
{
  char *arg;

  if (carmen_find_param(lvalue) > 0) 
    {
      if (carmen_find_param_pair(lvalue) == 0) 
	{
	  usage("Option '%s' requires argument: should be a string.\n", lvalue);
	  // In case the user provided a usage that doesn't exit.
	  exit(-1);
	}
      arg = carmen_param_pair(lvalue);
      return arg;
    }
  return NULL;
}

char *
carmen_process_param_file(char *lvalue, carmen_usage_func usage) 
{
  struct stat buf;
  char *arg;

  if (carmen_find_param(lvalue) > 0) 
    {
      if (carmen_find_param_pair(lvalue) == 0)
	usage("Option '%s' requires argument: should be on/off.\n", lvalue);
      arg = carmen_param_pair(lvalue);
      if (stat(arg, &buf) < 0) {
	usage("Option '%s', file %s not available: %s\n", lvalue, arg, strerror(errno));
	// In case the user provided a usage that doesn't exit.
	exit(-1);
      }
      if (!S_ISREG(buf.st_mode)) 
	{
	  usage("Option '%s' requires regular file. %s is not a regular file.\n", lvalue, arg);
	  // In case the user provided a usage that doesn't exit.
	  exit(-1);
	}
      return arg;
    }
  return NULL;  
}

char *
carmen_process_param_directory(char *lvalue, carmen_usage_func usage) 
{
  struct stat buf;
  char *arg;

  if (carmen_find_param(lvalue) > 0) 
    {
      if (carmen_find_param_pair(lvalue) == 0) 
	{
	  usage("Option '%s' requires argument: should be on/off.\n", lvalue);
	  // In case the user provided a usage that doesn't exit.
	  exit(-1);
	}
      arg = carmen_param_pair(lvalue);
      if (stat(arg, &buf) < 0)
	{
	  usage("Option '%s', file %s not available: %s\n", lvalue, arg, strerror(errno));
	  // In case the user provided a usage that doesn't exit.
	  exit(-1);
	}
      if (!S_ISDIR(buf.st_mode))
	{
	  usage("Option '%s' requires directorny name. %s is not a directory.\n", lvalue, arg);
	  // In case the user provided a usage that doesn't exit.
	  exit(-1);
	}
      return arg;
    }
  return NULL;
}

int 
carmen_read_commandline_parameters(int argc, char **argv)
{
  int i;
  int last_commandline_arg = argc;
  char *tmp_arg1;
  
  if (argc == 1)
    return 1;

  for (i = 1; i < last_commandline_arg; i++)
    {
      if (argv[i][0] != '-') {

	if (i < last_commandline_arg && i+1 < argc) {
	  tmp_arg1 = argv[i];
	  memmove(argv+i, argv+i+1, (argc-i-1)*sizeof(char *));
	  argv[argc-1] = tmp_arg1;
	  i--;
	}
	last_commandline_arg--;

	continue;
      }

      /* If it's the last argument, or the next argument is -<letter>,
	 then this obviously is not a param pair. 

	 Note that we test isalpha. and not isalphnum, so that we can pass 
	 -<digit> to the the param pair code below. */

      if (i + 1 == argc || (strlen(argv[i+1]) > 1 &&
			    argv[i + 1][0] == '-' && isalpha(argv[i + 1][1])))
	{
	  /* single parameter */

	  if (strcmp(argv[i], "-v") == 0) 
	    carmen_carp_verbose = 1; 
	  else
	    {
	      strcpy(param_list[param_num].robot, "commandline");
	      strcpy(param_list[param_num].lvalue, argv[i] + 1);
	      strcpy(param_list[param_num].rvalue, "");
	      param_num++;
	    }	  
	}
      else 
	{
	  /* parameter pair */
	  strcpy(param_list[param_num].robot, "commandline");
	  strcpy(param_list[param_num].lvalue, argv[i] + 1);
	  strcpy(param_list[param_num].rvalue, argv[i + 1]);
	  param_num++;
	  i++;
	}
    }

  return last_commandline_arg;
}

char *
carmen_find_robot_name(int argc, char **argv)
{
  int i, j;

  for(i = 0; i < argc; i++)
    if(strcmp(argv[i], "-robot") == 0 && i + 1 < argc && argv[i + 1][0] != '-')
      return(argv[i + 1]);
  for(i = 0; i < argc; i++)
    for(j = 0; j < NUM_ROBOT_NAMES; j++)
      if(argv[i][0] == '-' && strcmp(argv[i] + 1, robot_names[j]) == 0)
	return(robot_names[j]);
  return NULL;
}

double 
carmen_get_time(void)
{
  struct timeval tv;
  double t;

  if (gettimeofday(&tv, NULL) < 0) 
    carmen_warn("carmen_get_time encountered error in gettimeofday : %s\n",
		strerror(errno));
  t = tv.tv_sec + tv.tv_usec/1000000.0;
  return t;
}

char *carmen_get_host(void) 
{
  FILE *bin_host;
  char hostname[1024];

  if (getenv("HOST") == NULL) {
    if (getenv("HOSTNAME") != NULL)       
      setenv("HOST", getenv("HOSTNAME"), 1);
    else if (getenv("host") != NULL)       
      setenv("HOST", getenv("host"), 1);
    else if (getenv("hostname") != NULL)       
      setenv("HOST", getenv("hostname"), 1);
    else {
      bin_host = popen("/bin/hostname", "r");
      if (bin_host == NULL)
	carmen_die("\n\tCan't get machine name from $HOST, $host, $hostname or /bin/hostname.\n"
		   "\tPlease set one of these environment variables properly.\n\n");      
      if (fscanf(bin_host, "%s", hostname) != 1) {
	carmen_die("\n\tCan't get machine name from $HOST, $host, $hostname or /bin/hostname.\n"
		   "\tPlease set one of these environment variables properly.\n\n");      
      }
      setenv("HOST", hostname, 1);
      pclose(bin_host);
    }
  }

  return getenv("HOST");
}

carmen_default_message *carmen_default_message_create(void)
{
  if (static_message.host == NULL) 
    static_message.host = carmen_get_host();
  static_message.timestamp = carmen_get_time();

  return &static_message;
}

char *
carmen_extract_filename(char *path)
{
  /* remove any leading path from the program name */
  if(strrchr(path, '/') != NULL) {
    path = strrchr(path, '/');
    path++;
  }
  
  return path;
}


static FILE *carmen_carp_output = NULL;

void 
carmen_perror(const char* fmt, ...) {
  va_list args;

  if (carmen_carp_output == NULL)
    carmen_carp_output = stderr;

  va_start(args, fmt);
  vfprintf(carmen_carp_output, fmt, args);
  va_end(args);
  fprintf(carmen_carp_output, " : %s\n", strerror(errno));
  fflush(carmen_carp_output);
}

void 
carmen_die(const char* fmt, ...) {
  va_list args;

  if (carmen_carp_output == NULL)
    carmen_carp_output = stderr;

  va_start(args, fmt);
  vfprintf(carmen_carp_output, fmt, args);
  va_end(args);
  fflush(carmen_carp_output);
  exit(-1);
}

void 
carmen_die_syserror(const char* fmt, ...) {
  va_list args;

  if (carmen_carp_output == NULL)
    carmen_carp_output = stderr;

  va_start(args, fmt);
  vfprintf(carmen_carp_output, fmt, args);
  va_end(args);
  fprintf(carmen_carp_output, " : %s\n", strerror(errno));
  fflush(carmen_carp_output);

  exit(-1);
}

void 
carmen_warn(const char* fmt, ...) {
  va_list args;

  if (carmen_carp_output == NULL)
    carmen_carp_output = stderr;

  va_start(args, fmt);
  vfprintf(carmen_carp_output, fmt, args);
  va_end(args);
  fflush(carmen_carp_output);
}

void 
carmen_verbose(const char *fmt, ...) {
  va_list args;

  if (!carmen_carp_verbose)
    return;

  if (carmen_carp_output == NULL)
    carmen_carp_output = stderr;

  va_start(args, fmt);
  vfprintf(carmen_carp_output, fmt, args);
  va_end(args);
  fflush(carmen_carp_output);
}

void 
carmen_carp_set_output(FILE *output) {
  carmen_carp_output = output;
}

void 
carmen_carp_set_verbose(int verbosity) {
  carmen_carp_verbose = verbosity;
}

int
carmen_carp_get_verbose(void) {
  return carmen_carp_verbose;
}

extern IPC_VERBOSITY_TYPE ipcVerbosity;

void carmen_running_average_clear(carmen_running_average_t *average)
{
  int i;

  for(i = 0; i < AVERAGE_LENGTH; i++)
    average->data[i] = 0.0;
  average->index = 0;
  average->sum = 0.0;
  average->count = 0;
}

void carmen_running_average_add(carmen_running_average_t *average, double x)
{
  average->sum -= average->data[average->index];
  average->data[average->index] = x;
  average->sum += x;
  average->index++;
  if(average->index == AVERAGE_LENGTH)
    average->index = 0;
  if(average->count < AVERAGE_LENGTH)
    average->count++;
}

double carmen_running_average_report(carmen_running_average_t *average)
{
  return (average->sum / (double)average->count);
}

carmen_inline int
carmen_round(double X) 
{
  if (X >= 0)
    return (int)(X + 0.5);
  else
    return (int)(X - 0.5);
}

carmen_inline double
carmen_clamp(double X, double Y, double Z) 
{
  if (Y < X)
    return X;
  else if (Y > Z)
    return Z;
  return Y;
}

carmen_inline int
carmen_trunc(double X) 
{
  return (int)(X);
}

carmen_inline int
carmen_imin(int val1, int val2) 
{
  if (val2 < val1)
    return val2;
  return val1;
}

carmen_inline int 
carmen_imax(int val1, int val2) 
{
  if (val2 > val1)
    return val2;
  return val1;
}

carmen_inline double 
carmen_fmin(double val1, double val2) 
{
  if (val2 < val1)
    return val2;
  return val1;
}

carmen_inline double 
carmen_fmax(double val1, double val2) 
{
  if (val2 > val1)
    return val2;
  return val1;
}

carmen_inline double 
carmen_square(double val)
{
  return (val*val);
}

carmen_inline double
carmen_normalize_theta(double theta) 
{
  double multiplier;

  if (theta >= -M_PI && theta < M_PI)
    return theta;

  multiplier = floor(theta / (2*M_PI));
  theta = theta - multiplier*2*M_PI;
  if (theta >= M_PI)
    theta -= 2*M_PI;
  if (theta < -M_PI)
    theta += 2*M_PI;

  return theta;
} 

carmen_inline void carmen_erase_structure(void* ptr, int size_of_struture)
{
  memset(ptr, 0, size_of_struture);
}


carmen_inline double 
carmen_knots_to_meters_per_second(double knots)
{
  /// KNOTS_TO_METERS_PER_SECOND 0.5148
  return (0.5148 * knots);
}


carmen_inline double 
carmen_radians_to_degrees(double theta) 
{
  return (theta * 180.0 / M_PI);
}

carmen_inline double
carmen_degrees_to_radians(double theta) 
{
  return (theta * M_PI / 180.0);
}

carmen_inline double
carmen_distance_traj(carmen_traj_point_p p1, carmen_traj_point_p p2) 
{
  return sqrt((p1->x-p2->x)*(p1->x-p2->x) + (p1->y-p2->y)*(p1->y-p2->y));
}

carmen_inline double
carmen_distance(carmen_point_p p1, carmen_point_p p2) 
{
  return sqrt((p1->x-p2->x)*(p1->x-p2->x) + (p1->y-p2->y)*(p1->y-p2->y));
}

carmen_inline double
carmen_angle_between(carmen_traj_point_p p1, carmen_traj_point_p p2) 
{
  return atan2(p2->y - p1->y, p2->x - p1->x);
}

void 
carmen_get_bresenham_parameters(int p1x, int p1y, int p2x, int p2y, carmen_bresenham_param_t *params) 
{
  params->UsingYIndex = 0;

  if (fabs((double)(p2y-p1y)/(double)(p2x-p1x)) > 1)
    (params->UsingYIndex)++;

  if (params->UsingYIndex) 
    {
      params->Y1=p1x;
      params->X1=p1y;
      params->Y2=p2x;
      params->X2=p2y;
    } 
  else 
    {
      params->X1=p1x;
      params->Y1=p1y;
      params->X2=p2x;
      params->Y2=p2y;
    }

  if ((p2x - p1x) * (p2y - p1y) < 0) 
    {
      params->Flipped = 1;
      params->Y1 = -params->Y1;
      params->Y2 = -params->Y2;
    } 
  else
    params->Flipped = 0;
  
  if (params->X2 > params->X1)
    params->Increment = 1;
  else
    params->Increment = -1;

  params->DeltaX=params->X2-params->X1;
  params->DeltaY=params->Y2-params->Y1;

  params->IncrE=2*params->DeltaY*params->Increment;
  params->IncrNE=2*(params->DeltaY-params->DeltaX)*params->Increment;
  params->DTerm=(2*params->DeltaY-params->DeltaX)*params->Increment;

  params->XIndex = params->X1;
  params->YIndex = params->Y1;
}

carmen_inline void 
carmen_get_current_point(carmen_bresenham_param_t *params, int *x, int *y) 
{ 
  if (params->UsingYIndex) 
    {
      *y = params->XIndex;
      *x = params->YIndex;
      if (params->Flipped)
	*x = -*x;
    } 
  else 
    {
      *x = params->XIndex;
      *y = params->YIndex;
      if (params->Flipped)
	*y = -*y;
    }
}

carmen_inline int 
carmen_get_next_point(carmen_bresenham_param_t *params) 
{
  if (params->XIndex == params->X2)
    {
      return 0;
    }
  params->XIndex += params->Increment;
  if (params->DTerm < 0 || (params->Increment < 0 && params->DTerm <= 0))     
    params->DTerm += params->IncrE;
  else 
    {
      params->DTerm += params->IncrNE;
      params->YIndex += params->Increment;
    }
  return 1;
}

int 
carmen_sign(double num) 
{
  if (num >= 0)
    return 1;
  return -1;
}

void 
carmen_rect_to_polar(double x, double y, double *r, double *theta)
{
  *r = hypot(x, y);
  *theta = atan2(y, x);
}

void
carmen_rotate_2d(double *x, double *y, double theta)
{
  double x2 = *x;

  *x = cos(theta)*(*x) - sin(theta)*(*y);
  *y = sin(theta)*x2 + cos(theta)*(*y);
}

unsigned int
carmen_generate_random_seed(void)
{
  FILE *random_fp;
  unsigned int seed;
  int ints;

  random_fp = fopen("/dev/random", "r");
  if (random_fp == NULL) {
    carmen_warn("Could not open /dev/random for reading: %s\n"
                "Using time ^ PID\n", strerror(errno));
    seed = time(NULL) ^ getpid();
    srandom(seed);
    return seed;
  }

  ints = fread(&seed, sizeof(int), 1, random_fp);
  if (ints != 1) {
    carmen_warn("Could not read an int from /dev/random: %s\n"
                "Using time ^ PID\n", strerror(errno));
    seed = time(NULL) ^ getpid();
    srandom(seed);
    return seed;
  }

  fclose(random_fp);

  srandom(seed);

  return seed;
}

unsigned int
carmen_randomize(int *argc, char ***argv) 
{
  long long int user_seed;
  unsigned int seed;
  int bytes_to_move;
  int i;
  char *endptr;

  for (i = 0; i < *argc-1; i++) {
    if (strcmp((*argv)[i], "--seed") == 0) {
      user_seed = strtoll((*argv)[i+1], &endptr, 0);
      seed = (unsigned int)user_seed;
      if (endptr && *endptr != '\0') {
	carmen_warn("Bad random seed %s.\n", (*argv)[i+1]);
	seed = carmen_generate_random_seed();
      } else if (seed != user_seed) {
	carmen_warn("Random seed too large: %s.\n", (*argv)[i+1]);
	seed = carmen_generate_random_seed();
      } else {
	if (i < *argc-2) {
	  bytes_to_move = (*argc-2-i)*sizeof(char *);
	  memmove((*argv)+i, (*argv)+i+2, bytes_to_move);
	}
	(*argc) -= 2;	
	srandom(seed);
      }
      return seed;
    }
  }
  seed = carmen_generate_random_seed();
  return seed;
}

void 
carmen_set_random_seed(unsigned int seed)
{
  srand(seed);
}

/*
	From the rand(3) man page:

	In Numerical Recipes in C: The Art of Scientific Computing 
	(William H. Press, Brian P.  Flannery, Saul A. Teukolsky, 
	William T. Vetterling; New York: Cambridge University Press, 
	1992 (2nd ed., p. 277)), the following comments are made:
	"If you want to generate a random integer  between  1  and  10,  
	you  should always do it by using high-order bits, as in

        j=1+(int) (10.0*rand()/(RAND_MAX+1.0));

	and never by anything resembling

        j=1+(rand() % 10);

	(which uses lower-order bits)."
*/

int 
carmen_int_random(int max)
{
  return (int)(max*(rand()/(RAND_MAX+1.0)));
}

double 
carmen_uniform_random(double min, double max)
{
  return min + (rand() / (double)RAND_MAX) * (max - min);
}

double 
carmen_gaussian_random(double mean, double std)
{
  const double norm = 1.0 / (RAND_MAX + 1.0);
  double u = 1.0 - rand() * norm;                  /* can't let u == 0 */
  double v = rand() * norm;
  double z = sqrt(-2.0 * log(u)) * cos(2.0 * M_PI * v);
  return mean + std * z;
} 

int
carmen_file_exists(const char *filename)
{
  FILE *fp;

  fp = fopen(filename, "r");
  if(fp == NULL)
    return 0;
  else {
    fclose(fp);
    return 1;
  }
}

char 
*carmen_file_extension(const char *filename)
{
  return strrchr(filename, '.');
}

static int
search_path_add(char *path)
{
  if (sp_num >= SP_SIZE)
    return -1;

  search_path[sp_num] = (char *) calloc(strlen(path) + 1, sizeof(char));
  carmen_test_alloc(search_path[sp_num]);
  strcpy(search_path[sp_num], path);
  sp_num++;
  return 0;
}

static void
init_search_path()
{
  char *carmen_home;
  char buf[128];
  int i;

  sp_num = 0;
  search_path_add(".");
  for (i = 0; i < rsp_num; i++) {
    sprintf(buf, "../%s", relative_search_path[i]);
    search_path_add(buf);
  }
  carmen_home = getenv("CARMEN_HOME");
  if (carmen_home) {
    for (i = 0; i < rsp_num; i++) {
      sprintf(buf, "%s/%s", carmen_home, relative_search_path[i]);
      search_path_add(buf);
    }
  }
  for (i = 0; i < rsp_num; i++) {
    sprintf(buf, "/usr/local/%s", relative_search_path[i]);
    search_path_add(buf);
  }
}

char
**carmen_get_search_path(int *num_paths)
{
  int i;
  char **sp;

  if (num_paths == NULL)
    return NULL;

  if (sp_num <= 0)
    init_search_path();

  sp = (char **) calloc(sp_num, sizeof(char *));
  carmen_test_alloc(sp);
  for (i = 0; i < sp_num; i++) {
    sp[i] = (char *) calloc(strlen(search_path[i]) + 1, sizeof(char));
    carmen_test_alloc(sp[i]);
    strcpy(sp[i], search_path[i]);
  }
  *num_paths = sp_num;
  return sp;
}

char
*carmen_file_find(const char *filename)
{
  char *path, buf[256];
  int i;
  FILE *f;

  if (sp_num <= 0)
    init_search_path();
  for (i = 0; i < sp_num; i++) {
    sprintf(buf, "%s/%s", search_path[i], filename);
    f = fopen(buf, "r");
    if (f != NULL) {
      path = (char *) calloc(strlen(buf) + 1, sizeof(char));
      carmen_test_alloc(path);
      strcpy(path, buf);
      fclose(f);
      return path;
    }
  }
  return NULL;
}

static int current_percent;

void 
carmen_global_start_progress_bar(char *label)
{
  fprintf(stderr, "%s : ", label);
  current_percent = 0;
}

void
carmen_global_end_progress_bar(void)
{
  if (current_percent > 0)
    fprintf(stderr, "[0Kdone\n");
  else
    fprintf(stderr, "done\n");
}

void 
carmen_global_update_progress_bar(int count, int size)
{
  char buffer[20];
  int percent = carmen_round(count*10.0/size);
  if (percent > 10)
    {
      carmen_warn("\nThere seems to be a bug in your call to %s, \n"
		  "because you called it with count > size. count truncated to size.\n",
		  __FUNCTION__);
      percent = 10;
    }
  if (percent > current_percent)
    {
      memset(buffer, '#', percent*sizeof(char));
      buffer[percent] = '\0';
      fprintf(stderr, "%s[%dD", buffer, percent);
      current_percent = percent;
    }
}

int
carmen_strcasecmp (const char *s1, const char *s2)
{
  const unsigned char *p1 = (const unsigned char *) s1;
  const unsigned char *p2 = (const unsigned char *) s2;
  unsigned char c1, c2;

  if (p1 == p2)
    return 0;

  do
    {
      c1 = tolower (*p1++);
      c2 = tolower (*p2++);
      if (c1 == '\0')
	break;
    }
  while (c1 == c2);

  return c1 - c2;
}

int
carmen_strncasecmp (const char *s1, const char *s2, size_t n)
{
  const unsigned char *p1 = (const unsigned char *) s1;
  const unsigned char *p2 = (const unsigned char *) s2;
  unsigned char c1, c2;

  if (p1 == p2 || n == 0)
    return 0;

  do
    {
      c1 = tolower (*p1++);
      c2 = tolower (*p2++);
      if (c1 == '\0' || c1 != c2)
	return c1 - c2;
    } while (--n > 0);
  
  return c1 - c2;
}

char *carmen_new_stringv(const char *fmt, va_list args)
{
  va_list ap;
  int n, size = 128;
  char *s;

  if (fmt == NULL)
    return NULL;

  s = (char *) calloc(size, sizeof(char));
  carmen_test_alloc(s);
  
  while (1) {
    va_copy(ap, args);
    n = vsnprintf(s, size, fmt, ap);
    va_end(ap);
    if (n < 0) {
      free(s);
      return NULL;
    }
    if (n >= 1 && n < size)
      return s;
    if (n >= 1)     // glibc 2.1
      size = n+1;
    else           // glibc 2.0
      size *= 2;
    s = (char *) realloc(s, size * sizeof(char));
    carmen_test_alloc(s);
  }

  return NULL;
}

char *carmen_new_string(const char *fmt, ...)
{
  va_list ap;
  char *s;

  va_start(ap, fmt);
  s = carmen_new_stringv(fmt, ap);
  va_end(ap);

  return s;
}

void carmen_print_version(void)
{
  fprintf(stderr, "CARMEN - Carnegie Mellon Robot Navigation Toolkit - ");
  fprintf(stderr, "Version %d.%d.%d\n\n", CARMEN_MAJOR_VERSION, 
	  CARMEN_MINOR_VERSION, CARMEN_REVISION);
}

// Patched offsets line processing provided by 
// Mathew Brewer <mbrewer@cs.umass.edu>

int
carmen_parse_sonar_offsets(char *offset_string, carmen_point_p offsets,
			   int num_sonars)
{
  int sonar_num=0;
  char *curr_val;

  if (!offset_string || !offsets)
    {
      carmen_warn("Bug in carmen_parse_sonar_offsets: a pointer arg was "
		  "passed as NULL\n");
      return -1;
    }

  curr_val = offset_string;
  do {
    //get X co-ordinate
    sscanf(curr_val, "%lf", &(offsets[sonar_num].x));
    if(curr_val==NULL){
      carmen_warn("Too few arguments in sonar offset string.\n");
      return -1;
    }
    curr_val = strchr(curr_val, ' ');
    if(curr_val==NULL){
      carmen_warn("Too few arguments in sonar offset string.\n");
      return -1;
    }
    for(;*curr_val!='\0' && *curr_val==' ';curr_val++);
    
    //get Y co-ordinate
    sscanf(curr_val, "%lf", &(offsets[sonar_num].y));
    if(curr_val==NULL){
      carmen_warn("Too few arguments in sonar offset string.\n");
      return -1;
    }
    curr_val = strchr(curr_val, ' ');
    if(curr_val==NULL){
      carmen_warn("Too few arguments in sonar offset string.\n");
      return -1;
    }
    for(;*curr_val!='\0' && *curr_val==' ';curr_val++);
    
    //get theta co-ordinate
    sscanf(curr_val, "%lf", &(offsets[sonar_num].theta));
    if(sonar_num+1==num_sonars) {sonar_num++; break;}

    if(curr_val==NULL){
      carmen_warn("Too few arguments in sonar offset string.\n");
      return -1;
    }
    curr_val = strchr(curr_val, ' ');
    if(curr_val==NULL){
      carmen_warn("Too few arguments in sonar offset string.\n");
      return -1;
    }
    for(;*curr_val!='\0' && *curr_val==' ';curr_val++);
    
    sonar_num++;
  } while (curr_val != NULL);

  if (sonar_num < num_sonars) {
    carmen_warn("Too few arguments in offset string.\n");
    return -1;
  }

  return 0;
}

int
carmen_parse_arm_joint_types(char *joint_string, carmen_arm_joint_t *joint_types,
			     int num_joints)
{
  char *s;
  int n, i;

  if (!joint_string || !joint_types)
    {
      carmen_warn("Bug in carmen_parse_arm_joint_types: a pointer arg was "
		  "passed as NULL\n");
      return -1;
    }
  
  s = joint_string;

  for (i = 0; i < num_joints; i++) {
    s += strspn(s, " \t");
    if (strlen(s) == 0) {
      carmen_warn("Too few arguments in joint types string.\n");
      return -1;
    }
    n = strcspn(s, " \t");
    if (!carmen_strncasecmp(s, "motor", n))
      joint_types[i] = CARMEN_MOTOR;
    else if (!carmen_strncasecmp(s, "servo", n))
      joint_types[i] = CARMEN_SERVO;
    else {
      carmen_warn("Bad argument (#%d) in joint types string.\n", i+1);
      return -1;
    }
  }

  return 0;
}


int 
carmen_terminal_cbreak(int blocking)
{
  struct termios buf;
  int err;

  err = tcgetattr(STDOUT_FILENO, &buf);
  if (err < 0)
    {
      carmen_perror("Could not get terminal attributes, no cbreak");
      return -1;
    }

  buf.c_lflag &= ~ICANON;
  buf.c_iflag &= ~ICRNL;
  buf.c_lflag |= ISIG;
  buf.c_cc[VMIN] = 1;
  buf.c_cc[VTIME] = 0;

  err = tcsetattr(STDOUT_FILENO, TCSADRAIN, &buf);
  if (err < 0)
    {
      carmen_perror("Could not set terminal attributes, no cbreak");
      return -1;
    }

  
  if (blocking) 
    return 0;

  err = fcntl(STDIN_FILENO, F_SETFL, O_NONBLOCK);
  if (err < 0)
    {
      carmen_perror("Could not fcntl, STDIN left nonblocking");
      return -1;
    }

  return 0;
}

int 
carmen_terminal_restore(void)
{
  struct termios buf;
  int err;
  long flags;

  err = tcgetattr(STDOUT_FILENO, &buf);
  if (err < 0)
    {
      carmen_perror("Could not get terminal attributes, no cbreak");
      return -1;
    }

  buf.c_lflag |= ICANON;
  buf.c_iflag |= ICRNL;

  err = tcsetattr(STDOUT_FILENO, TCSADRAIN, &buf);
  if (err < 0)
    {
      carmen_perror("Could not set terminal attributes, no cbreak");
      return -1;
    }

  err = fcntl(STDIN_FILENO, F_GETFL, &flags);
  if (err < 0)
    {
      carmen_perror("Could not fcntl get, STDIN not set to blocking");
      return -1;
    }
  
  flags = flags & ~O_NONBLOCK;

  err = fcntl(STDIN_FILENO, F_SETFL, flags);
  if (err < 0)
    {
      carmen_perror("Could not fcntl, STDIN not set to blocking");
      return -1;
    }

  return 0;
}

carmen_list_t *carmen_list_create(int entry_size, int initial_capacity)
{
  carmen_list_t *list;

  list = (carmen_list_t *)calloc(1, sizeof(carmen_list_t));
  carmen_test_alloc(list);
  list->entry_size = entry_size;
  
  list->capacity = initial_capacity;
  if (initial_capacity > 0)
    list->list = (void *)calloc(initial_capacity, entry_size);
  carmen_test_alloc(list);
  
  return list;
}

carmen_list_t *carmen_list_create_from_data(int entry_size, int num_elements, 
					    void *data)
{
  carmen_list_t *list;

  list = (carmen_list_t *)calloc(1, sizeof(carmen_list_t));
  carmen_test_alloc(list);
  list->entry_size = entry_size;  
  list->capacity = num_elements;
  list->length = num_elements;  
  list->list = data;
  
  return list;

}

carmen_list_t *carmen_list_duplicate(carmen_list_t *list)
{
  carmen_list_t *new_list;

  new_list = (carmen_list_t *)calloc(1, sizeof(carmen_list_t));
  carmen_test_alloc(new_list);
  new_list->entry_size = list->entry_size;
  if (list->length > 0) {
    new_list->capacity = list->length;
    new_list->length = list->length;
    new_list->list = (void *)calloc(new_list->capacity, new_list->entry_size);
    carmen_test_alloc(new_list->list);
    memcpy(new_list->list, list->list, new_list->length*new_list->entry_size);
  } else {
    new_list->capacity = 10;
    new_list->length = 0;
    new_list->list = (void *)calloc(new_list->capacity, new_list->entry_size);
    carmen_test_alloc(new_list->list);
  }
  return new_list;
}

void carmen_list_add(carmen_list_t *list, void *entry)
{
  if (list->length == list->capacity) {
    list->capacity = list->capacity+10;
    list->list = realloc(list->list, list->capacity*list->entry_size);
    carmen_test_alloc(list->list);
    memset(list->list+list->length*list->entry_size, 0, 
	   (list->capacity-list->length)*list->entry_size);
  }
  
  memcpy(list->list+list->length*list->entry_size, entry, list->entry_size);
  list->length++;
}

void carmen_list_insert(carmen_list_t *list, void *entry, int i)
{
  if (i >= list->length) {
    carmen_warn("carmen_list_insert called with argument %d greater than "
		"length: %d\n This is a bug in the calling function.\n"
		"List not changed.\n", i, list->length);
    return;
  }

  if (list->length == list->capacity) {
    list->capacity = list->capacity+10;
    list->list = realloc(list->list, list->capacity*list->entry_size);
    carmen_test_alloc(list->list);
    memset(list->list+list->length*list->entry_size, 0, 
	   (list->capacity-list->length)*list->entry_size);
  }

  memmove(list->list+(i+1)*list->entry_size, list->list+i*list->entry_size,
	  (list->length-i)*list->entry_size);
  memcpy(list->list+i*list->entry_size, entry, list->entry_size);
  list->length++;
}

int carmen_list_length(carmen_list_t *list) 
{
  return list->length;
}

void carmen_list_delete(carmen_list_t *list, int entry_num)
{
  list->length--;
  
  if (entry_num < list->length)
    memcpy(list->list+entry_num*list->entry_size, 
	   list->list+(entry_num+1)*list->entry_size, 
	   list->entry_size*(list->length-entry_num));
}

void *carmen_list_get(carmen_list_t *list, int entry_num)
{
  return list->list+entry_num*list->entry_size;
}

void carmen_list_destroy(carmen_list_t **list)
{
  if ((*list)->list)
    free((*list)->list);
  free(*list);
  *list = NULL;
}

void carmen_list_set(carmen_list_t *list, int entry_num, void *entry)
{
  if (list->capacity < entry_num) {
    list->capacity = entry_num+1;
    list->list = realloc(list->list, list->capacity*list->entry_size);
    carmen_test_alloc(list->list);
    memset(list->list+list->length*list->entry_size, 0, 
	   (list->capacity-list->length)*list->entry_size);
  }
  
  memcpy(list->list+entry_num*list->entry_size, entry, list->entry_size);
  if (list->length <= entry_num) 
    list->length = entry_num+1;
}

void carmen_eigs_to_covariance(double theta, double major, double minor,
			       double *vx, double *vxy, double *vy)
{
  double cos_theta, sin_theta;

  cos_theta = cos(theta);
  sin_theta = sin(theta);

  *vx = major*cos_theta*cos_theta + minor*sin_theta*sin_theta;
  *vy = major*sin_theta*sin_theta + minor*cos_theta*cos_theta;

  *vxy = -major*sin_theta*cos_theta + minor*sin_theta*cos_theta;
}

carmen_inline char *carmen_next_word(char *str)
{
  char *mark = str;

  if(str == NULL)
    return NULL;
  while(*mark != '\0' && !(*mark == ' ' || *mark == '\t'))
    mark++;
  while(*mark != '\0' &&  (*mark == ' ' || *mark == '\t'))
    mark++;
  return mark;
}

carmen_inline char *carmen_next_n_words(char *str, int n)
{
  int i;
  char *result;

  result = str;
  for(i = 0; i < n; i++)
    result = carmen_next_word(result);
  return result;
}

double carmen_global_convert_degmin_to_double(double dm_format) {
  double degree   = floor(dm_format / 100.0);
  double minutes  = (dm_format - degree*100.0) / 60.0;
  return degree + minutes;
}

int carmen_parse_bumper_offsets(char *offset_string, carmen_position_p offsets, int num_bumpers)
{
  int bumper_num=0;
  char *curr_val;

  if (!offset_string || !offsets)
    {
      carmen_warn("Bug in carmen_parse_bumper_offsets: a pointer arg was "
		  "passed as NULL\n");
      return -1;
    }

  curr_val = offset_string;
  do {
    //get X co-ordinate
    sscanf(curr_val, "%lf", &(offsets[bumper_num].x));
    if(curr_val==NULL){
      carmen_warn("Too few arguments in bumper offset string.\n");
      return -1;
    }
    curr_val = strchr(curr_val, ' ');
    if(curr_val==NULL){
      carmen_warn("Too few arguments in bumper offset string.\n");
      return -1;
    }
    for(;*curr_val!='\0' && *curr_val==' ';curr_val++);
    
    //get Y co-ordinate
    sscanf(curr_val, "%lf", &(offsets[bumper_num].y));
    if(bumper_num+1==num_bumpers) {bumper_num++; break;}
    if(curr_val==NULL){
      carmen_warn("Too few arguments in bumper offset string.\n");
      return -1;
    }
    curr_val = strchr(curr_val, ' ');
    if(curr_val==NULL){
      carmen_warn("Too few arguments in bumper offset string.\n");
      return -1;
    }
    for(;*curr_val!='\0' && *curr_val==' ';curr_val++);
    
    bumper_num++;
  } while (curr_val != NULL);

  if (bumper_num < num_bumpers) {
    carmen_warn("Too few arguments in offset string.\n");
    return -1;
  }

  return 0;
}

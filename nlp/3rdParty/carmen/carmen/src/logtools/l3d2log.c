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

#include <carmen/carmen.h>
#include <carmen/logtools.h>

void
print_usage( void )
{
  fprintf( stderr, "\nusage: l3d2log <LOG-FILE> <LOG-FILE>\n  Converte for Log3D log files of Dirk Haehnel into CARMEN log files.\n"  );
}

/**************************************************************************
 * MAIN-LOOP
 **************************************************************************/

int
main(int argc, char *argv[])
{
  logtools_log_data_t   log;
  int                   i;

  if (argc<3) {
    print_usage();
    exit(1);
  }
  
  for (i=1; i<argc-2; i++) {
    {
      print_usage();
      exit(1);
    }
  }
  
  if (!logtools_read_logfile( &log, argv[argc-2] ))
      exit(1);

  if (!logtools_write_logfile( &log, argv[argc-1] ))
      exit(1);
  
  exit(0);
}

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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <math.h>
#include <unistd.h>
#include <termios.h>
#include <fcntl.h>
#include <sys/signal.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/ioctl.h>

#include <carmen/carmen.h>
#include <carmen/gps_nmea_interface.h>

#include "gps.h"
#include "gps-ipc.h"
#include "gps-io.h"


void
read_parameters(SerialDevice *dev, int argc, char **argv)
{
  char* device;

  carmen_param_t gps_dev[] = {
    {"gps", "nmea_dev",  CARMEN_PARAM_STRING, &device, 0, NULL},
    {"gps", "nmea_baud", CARMEN_PARAM_INT,    &(dev->baud),    0, NULL}};
  
  carmen_param_install_params(argc, argv, gps_dev, 
			      sizeof(gps_dev) / sizeof(gps_dev[0]));
  
  strncpy( dev->ttyport, device, MAX_NAME_LENGTH );

  free(device);

}

void
print_usage( void )
{
  //  fprintf( stderr, "gps-nmea [-nr NR] [-dev DEVICE]\n");
  fprintf( stderr, "Syntax: gps-nmea\n");
}

/**************************************************************************
 * MAIN-LOOP
 **************************************************************************/

int
main(int argc, char *argv[])
{
  int                         gps_nr = 0;
  SerialDevice                dev;
  carmen_gps_gpgga_message    gpgga;
  carmen_gps_gprmc_message    gprmc;

  carmen_erase_structure(&gpgga, sizeof(carmen_gps_gpgga_message) );
  carmen_erase_structure(&gprmc, sizeof(carmen_gps_gprmc_message) );
  
  gpgga.host = carmen_get_host();
  gprmc.host = carmen_get_host();
  DEVICE_init_params( &dev );

  carmen_ipc_initialize( argc, argv );
  ipc_initialize_messages();
 
  read_parameters( &dev, argc, argv );

  carmen_extern_gpgga_ptr = &gpgga;
  carmen_extern_gpgga_ptr->nr = gps_nr;
  carmen_extern_gprmc_ptr = &gprmc;
  carmen_extern_gprmc_ptr->nr = gps_nr;

  fprintf( stderr, "INFO: ************************\n" );
  fprintf( stderr, "INFO: ********* GPS   ********\n" );
  fprintf( stderr, "INFO: ************************\n" );

  fprintf( stderr, "INFO: open device: %s\n", dev.ttyport );
  if (DEVICE_connect_port( &dev )<0) {
    fprintf( stderr, "ERROR: can't open device !!!\n\n" );
    exit(1);
  } else {
    fprintf( stderr, "INFO: done\n" );
  }

  while(TRUE) {

    if ( DEVICE_bytes_waiting( dev.fd )>10 ) {
      if (DEVICE_read_data( dev )) {
	gpgga.timestamp = carmen_get_time();
	gprmc.timestamp = carmen_get_time();

	ipc_publish_position();
      }
      usleep(100000);
    } else {
      carmen_ipc_sleep(0.25);
      //IPC_listen(0);
      //usleep(250000);
    }

  }

  return(0);
}

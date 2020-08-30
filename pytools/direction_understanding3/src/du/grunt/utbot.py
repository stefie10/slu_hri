"""
copied from usarsim from the pyro interface by stefie10
"""
import socket, thread, time, math, string

DEG2RAD = 3.14159 / 180.0
RAD2DEG = 180.0 / 3.1415

class UtbotError(Exception):
    def __init__(self, *args):
        Exception.__init__(self, *args)

class utbot:

    #--------------------------------------------------------------------------
    # functions for connection to Unreal Touranment(UT) server.
    #--------------------------------------------------------------------------

    def __init__(self, hostname='localhost', port=3000, auto=1, speed=20):
        """
    	connect to the Unreal Tournament server
        """ 

        # debugging information will be inhibited
        self.debug = None
        self.player_loc = None

        # make a connection to the specified UT server
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((hostname, port))
        self.__socket.setblocking(0)
        self.__inbuf = ''
        self.__translate = 0.0
        self.__rotate = 0.0
        self.__connected = 0
        self.fov = 0

        # create sensory data repository
        self.power		= {}
        self.pose   	= {}
        self.rotation	= {}
        self.velocity	= {}
        self.sonar		= {}
        self.sonarGeometry  = []
        self.sonarConfig    = {}
        self.laser		= {}
        self.laserConfig    = {}
        self.ptz		= {}
        self.ptzConfig  = {}
        self.ptzName    = ''
        self.ptzFrame   = ''
        self.rfid       = {}
        self.rfidReleaser = ''
        self.encoder    = {}
        self.encoderConfig  = {}
        self.gps		= {}
        self.bumper		= {}
        self.bumperGeometry	= {}
        self.truth		= {}


        # create automatic update thread
        self.lock = thread.allocate_lock()
        if auto: 
            self.start_update(speed)
        else: 
            self.stop_update()

        self.server = (hostname, port)
        if self.debug: print '<connected to %s:%d>' % self.server
        self.connect()
        self.turnon_debug()

    def connect(self):
        self.__connected = 1
    
    def disconnect(self):
        self.__connected = 0

    def close(self):
        """
    	disconnect from the Unreal Tournament server.
    	"""
        # close the connection
        if self.__socket is not None:
            try:
                self.__update_flag = 0
                self.__socket.shutdown(2)
                self.__socket.close()

	    except socket.error, errstr:
	        raise 'cannot close the socket: %s' % errstr

	    else:
		if self.debug: print '<connection to %s:%d is closed>' % self.server

    def pause(self):
        self.__sendline("PAUSE {TIME 10}")

        

    def spawn_bot(self, name, location_triple, rotation_triple):
    	"""
    	spawn a bot in UT
    	"""
        # send command
        args = (name,) +  location_triple + rotation_triple
        print "len", len(args)
        cmd = 'INIT {ClassName %s} {Location %.3f, %.3f, %.3f} {Rotation %.2f, %.2f, %.2f' % args
        self.__sendline(cmd)
        self.query_bot()
        # NO RESPONSE
        if self.debug: print '<spawn a bot>'+ cmd

    def query_bot(self):
        """
        collect information about the robot
        """
	try:
	    # Geometry information
	    time.sleep(0.2)
	    que = 'GETGEO {Type Sonar}'
	    self.__sendline(que)
	    if self.debug: print '<query>'+ que
	    time.sleep(0.2)
	    que = 'GETGEO {Type IR}'
	    self.__sendline(que)
	    if self.debug: print '<query>'+ que
	    time.sleep(0.2)
	    que = 'GETGEO {Type Touch}'
	    self.__sendline(que)
	    if self.debug: print '<query>'+ que
	    # Configuration information
	    time.sleep(0.2)
	    que = 'GETCONF {Type Sonar}'
	    self.__sendline(que)
	    if self.debug: print '<query>'+ que
	    time.sleep(0.2)
	    que = 'GETCONF {Type IR}'
	    self.__sendline(que)
	    if self.debug: print '<query>'+ que
	    time.sleep(0.2)
	    que = 'GETCONF {Type RangeScanner}'
	    self.__sendline(que)
	    if self.debug: print '<query>'+ que
	    time.sleep(0.2)
	    que = 'GETCONF {Type IRScanner}'
	    self.__sendline(que)
	    if self.debug: print '<query>'+ que
	    time.sleep(0.2)
	    que = 'GETCONF {Type Camera}'
	    self.__sendline(que)
	    if self.debug: print '<query>'+ que
	    time.sleep(0.2)
	    que = 'GETCONF {Type PanTilt}'
	    self.__sendline(que)
	    if self.debug: print '<query>'+ que
	    time.sleep(0.2)
	    que = 'GETCONF {Type RFIDReleaser}'
	    self.__sendline(que)
	    if self.debug: print '<query>'+ que
	    time.sleep(0.2)
	    que = 'GETCONF {Type Encoder}'
	    self.__sendline(que)
	    if self.debug: print '<query>'+ que
	    
	except:
	    raise 'cannot send query command'
        
    #--------------------------------------------------------------------------
    # functions for sensory information update.
    #--------------------------------------------------------------------------

    def __update_thread(self):
        """
	update sensory information (internal use only).
	"""
	if self.debug: print '<started a thread updating sensory information>'
	while self.__update_flag:
	    self.update()
	    time.sleep(1.0 / self.__update_speed)
	if self.debug: print '<stop the update thread>'


    def start_update(self, speed=20):
        """
	start to update sensory information continuously.
	"""
	self.__update_flag = 1
	self.__update_speed = speed


    def stop_update(self):
        """
	stop updating sensory information continuously.
	"""
	self.__update_flag = 0


    def update(self):
        """
	update sensory information.
	"""
	try:
	    # for synchronization with other functions
	    self.lock.acquire()

	    # update information
	    #for i in range(1):
	    while 1:
	        # read a packet
	        packet = self.__readline()
		if packet=='': 
                    break
		msg = utmessage(packet)
		if msg.head=='GEO':
		    geoType = msg.getFirstValue('Type')
		    if geoType[0]=='Sonar' or geoType[0]=='IR':
		        index = 0
		    	for s in msg.segs:
		    	    if s.has_key('Name'):
		    	        self.sonarGeometry.append(self.__toFloat(s['Location']))
		    	        self.sonarGeometry[index][2] = (self.__toDeg(s['Orientation']))[2]
		    	        index += 1
		    if geoType[0]=='Touch':
                        pass

		elif msg.head=='CONF':
		    confType = msg.getFirstValue('Type')
		    if confType[0]=='Sonar' and msg.getFirstValue('Name')!='':
	                self.sonarConfig['MaxRange'] = self.__toFloat(msg.getFirstValue('MaxRange'))
	                self.sonarConfig['BeamAngle'] = self.__toDeg(msg.getFirstValue('BeamAngle'))
		    if confType[0]=='IR' and msg.getFirstValue('Name')!='':
	                self.sonarConfig['MaxRange'] = self.__toFloat(msg.getFirstValue('MaxRange'))
		    if confType[0]=='RangeScanner' and msg.getFirstValue('Name')!='':
	                self.laserConfig['MaxRange'] = self.__toFloat(msg.getFirstValue('MaxRange'))
	                self.laserConfig['Resolution'] = self.__toDeg(msg.getFirstValue('Resolution'))
	                self.laserConfig['Fov'] = self.__toDeg(msg.getFirstValue('Fov'))
		    if confType[0]=='IRScanner' and msg.getFirstValue('Name')!='':
	                self.laserConfig['MaxRange'] = self.__toFloat(msg.getFirstValue('MaxRange'))
	                self.laserConfig['Resolution'] = self.__toDeg(msg.getFirstValue('Resolution'))
	                self.laserConfig['Fov'] = self.__toDeg(msg.getFirstValue('Fov'))
		    if confType[0]=='Camera' and msg.getFirstValue('Name')!='':
		        self.ptzName = (msg.getFirstValue('Name'))[0]
	                self.ptzConfig['DefFov'] = self.__toDeg(msg.getFirstValue('CameraDefFov'))
	                self.ptzConfig['MinFov'] = self.__toDeg(msg.getFirstValue('CameraMinFov'))
	                self.ptzConfig['MaxFov'] = self.__toDeg(msg.getFirstValue('CameraMaxFov'))
		    if confType[0]=='PanTilt' and msg.getFirstValue('Name')!='':
		        self.ptzFrame = (msg.getFirstValue('Name'))[0]
		    if confType[0]=='EFIDReleaser' and msg.getFirstValue('Name')!='':
		        self.rfidReleaser = (msg.getFirstValue('Name'))[0]
		    if confType[0]=='Encoder' and msg.getFirstValue('Name')!='':
		        self.encoderConfig['Resolution'] = self.__toDeg(msg.getFirstValue('Resolution'))
		elif msg.head=='STA':
		    # state message
		    self.power[0] = self.__toFloat(msg.getFirstValue('Battery'))
		    self.velocity[0] = self.__toFloat(msg.getFirstValue('Velocity'))
		    self.gps[0] = self.__toFloat(msg.getFirstValue('Location'))
		    self.truth[0] = self.gps[0]
		elif msg.head=='SEN':
		    # sensor message
		    senType = msg.getFirstValue('Type')
		    if senType[0]=='Sonar' or senType[0]=='IR':
		        index = 0
		    	for s in msg.segs:
		    	    if s.has_key('Range'):
		    	    	self.sonar[index] = self.__toFloat(s['Range'])
		    	    	index += 1
		    elif senType[0]=='RangeScanner' or senType[0]=='IRScanner':
    		        index = 0
		    	for s in msg.segs:
		    	    if s.has_key('Range'):
		    	    	self.laser[index] = self.__toFloat(s['Range'])
		    	    	index += 1
		    elif senType[0]=='Odometry':
		        self.pose[0] = self.__toFloat(msg.getFirstValue('Pose'))
		    elif senType[0]=='INU':
		        r = self.__toDeg(msg.getFirstValue('Orientation'))
		    	self.rotation[0] = r
			self.rotation[0][0] = r[1]
			self.rotation[0][1] = r[2]
			self.rotation[0][2] = r[0]
		    elif senType[0]=='RFID' or senType[0]=='VictRFID':
		        index = -1
		    	for s in msg.segs:
		    	    if s.has_key('ID'):
		    	    	index += 1
		    	        self.rfid[index] = {}
		    	    	self.rfid[index]['ID'] = s['ID']
		    	    if s.has_key('Status'):
		    	    	self.rfid[index]['Status'] = s['Status']
		    	    if s.has_key('Location'):
		    	    	self.rfid[index]['Location'] = self.__toFloat(s['Location'])
		    	#print self.rfid
		    elif senType[0]=='Encoder':
		        index = 0
		    	for s in msg.segs:
		    	    if s.has_key('Tick'):
		    	    	self.encoder[index] = self.__toInt(s['Tick'])
		    	    	index += 1
		    elif senType[0]=='Touch':
		        index = 0
		    	for s in msg.segs:
		    	    if s.has_key('Touch'):
		    	    	self.bumper[index] = bool(s['Touch'])
		    	    	index += 1
                    elif senType[0] == 'GroundTruth':
                        name = msg.getFirstValue("Name")[0]
                        if name == "GroundTruthPlayers":
                            x, y, z = [float(x) 
                                       for x in msg.getFirstValue("UTLocation")]
                            self.player_loc = x, y, z

		elif msg.head=='MIS':
		    idx=0
		    findCam=False
		    for s in msg.segs:
		        if s.has_key('Type'):
		            findCam= (s['Type'][0]=='PanTilt')
		        if findCam and s.has_key('Orientation'):
		            r = self.__toDeg(s['Orientation'])
		            if (idx>=1):
		                self.ptz[0][1] = self.ptz[0][2]
		                self.ptz[0][0] = r[1]
		                self.ptz[0][2] = r[2]
		            else:
		                self.ptz[0] = r
		            idx += 1
	            self.ptz[0][2]=self.fov
	            #print self.ptz[0]
		elif msg.head=='MISSTA':
                    print "MISSTA", msg
		elif msg.head=='RES':
		    resType = msg.getFirstValue('Type')
		    if resType[0]=='Camera':
		        self.fov = (self.__toDeg(msg.getFirstValue('Status')))[0]
		        self.ptz[0][2] = self.fov
		else:
		    print '<unknown message %s>' % msg.raw
	except socket.error:
	    # for synchronization with other functions
	    self.lock.release()
	    raise 'network connection error: (%d)' % (index)

	else:
	    # for synchronization with other functions
	    self.lock.release()


    #--------------------------------------------------------------------------
    # common functions for all devices (internal use only).
    #--------------------------------------------------------------------------

    def __repr__(self):
        """
	convert itself to a string.
	"""
	return 'utbot connected to %s:%d' % self.server


    def __readline(self) :
        if not self.__connected:
            raise UtbotError("Must be connected.")
        while 1:
            lf = string.find(self.__inbuf, '\n')
            if lf >= 0:
                break
            try:
                r = self.__socket.recv(4096)
            except:
                break
            if not r: 
                # connection broken
                break
            self.__inbuf = self.__inbuf + r
        if self.__inbuf=='':
            return ''
        else:
	    lf = lf - 1
            data = self.__inbuf[:lf]
            self.__inbuf = self.__inbuf[lf+2:]
            return data
    	

    def __sendline(self, data):
        """
	send the data string to the server.
	caller should catch exceptions for proper error handling,
	i.e. broken pipe.
	"""
	if not self.__connected:
	    return
	data = data + '\n\r'
	sent = 0
	while sent < len(data):
	    sent += self.__socket.send(data[sent:])

    def __toDeg(self, data):
        """
        transfer ut unit to degree
        """
        for i in range(len(data)):
            data[i] = float(data[i]) * RAD2DEG
        return data
    
    def __toInt(self, data):
        """
        transfer ut unit to degree
        """
        for i in range(len(data)):
            data[i] = int(data[i])
        return data

    def __toFloat(self, data):
        """
        transfer ut unit to degree
        """
        for i in range(len(data)):
            data[i] = float(data[i])
        return data

    def __getHitPos(self, bodyRot, botRelPos, botRelRot, dist):
        """
        bodyRot: robot rotation
        botRelPos: sensor position relative to robot body
        botRelRot: sensor rotation relative to robot body
        dist: range or distance
        """
        # new sensor position
    	orgP = self.__rotate(botRelPos,bodyRot)
    	
    	# hit position relative to sensor center
    	tmpP = [dist, 0.0, 0.0]
    	p = self.__rotate(tmpP,bodyRot)
    	relP = self.__rotate(p,botRelRot)
    	
    	# final hit position relative to robot body
    	hitP = [0.0, 0.0, 0.0]
    	hitP[0] = relP[0] + orgP[0]
    	hitP[1] = relP[1] + orgP[1]
    	hitP[2] = relP[2] + orgP[2]
        return hitP

    def __rotate(self, pos, rot):
        """
        rot[0]=pitch,rot[1]=yaw,rot[2]=roll
        rotate pos to a new position by 
        spin yaw => then spin pitch => then spin roll
        """
        b = rot[0] #pitch
        c = rot[1] #yaw
        a = rot[2] #roll
        matrix = []
        matrix.append([math.cos(b)*math.cos(c),-math.cos(b)*math.sin(c),math.sin(b)])
        matrix.append([math.cos(a)*math.sin(c)+math.sin(a)*math.sin(b)*math.cos(c),math.cos(a)*math.cos(c)-math.sin(a)*math.sin(b)*math.sin(c),-math.sin(a)*math.cos(b)])
        matrix.append([math.sin(a)*math.sin(c)-math.cos(a)*math.sin(b)*math.cos(c),math.sin(a)*math.cos(c)+math.cos(a)*math.sin(b)*math.sin(c),math.cos(a)*math.cos(b)])
        res = [0.0,0.0,0.0]
        res[0] = matrix[0][0]*pos[0] + matrix[0][1]*pos[1] + matrix[0][2]*pos[2]
        res[1] = matrix[1][0]*pos[0] + matrix[1][1]*pos[1] + matrix[1][2]*pos[2]
        res[2] = matrix[2][0]*pos[0] + matrix[2][1]*pos[1] + matrix[2][2]*pos[2]
        return res

    #--------------------------------------------------------------------------
    # functions for debugging.
    #--------------------------------------------------------------------------

    def turnon_debug(self):
        """
	show debugging information on the screen.
	"""
	self.debug = 1


    def turnoff_debug(self):
        """
	do not show debugging information on the screen.
	"""
	self.debug = None


    def dump_sensors(self): #--------------------------------------------------
        """
	print sensory information on the screen.
	"""
	print self.power
	print self.pose
	print self.rotation
	print self.velocity
	print self.sonar
	print self.laser
	print self.ptz
	print self.rfid
	print self.encoder
	print self.bumper
	print self.gps
	print self.truth


    #--------------------------------------------------------------------------
    # interfaces for the 'position' device.
    #--------------------------------------------------------------------------
    def set_speed(self, xspeed=None, yspeed=None, yawspeed=None,
                  xpos=None, ypos=None, yawpos=None, index=0):
	"""
	change the speed and the position. If a new value is None, the current
	sensor value will be used.
	"""
	try:
	    # send command
	    if xspeed is None:
	        xspeed = self.__translate
	    if yawspeed is None:
	        yawspeed = self.__rotate
	    left = xspeed * 3 - yawspeed * 2
	    right = xspeed * 3 + yawspeed * 2
	    cmd = "DRIVE {Left %f} {Right %f}" % (left,right)
	    self.__sendline(cmd)
	    self.__translate = xspeed
	    self.__rotate = yawspeed
	    # NO RESPONSE
	    if self.debug: print '<set the speed and position to (%d,%d,%d) and (%d,%d,%d)>' \
                    % (xspeed, yspeed, yawspeed, xpos, ypos, yawpos)
	except:
	    raise 'cannot set a speed and a position'


    #--------------------------------------------------------------------------
    # interfaces for the 'sonar' device.
    #--------------------------------------------------------------------------

    def get_sonar_geometry(self):
        """
	read the current geometry information of sonar sensors.
	"""
	return self.sonarGeometry

    def get_sonar_config(self):
        """
	read the current configuration of laser sensors.
	"""
	return self.sonarConfig

    def turnon_sonar(self):
        """
	turon on sonar transducers.
	
	"""
	pass

    def turnoff_sonar(self):
        """
	turon off sonar transducers.
	
	"""
	pass

    #--------------------------------------------------------------------------
    # interfaces for the 'laser' device.
    #--------------------------------------------------------------------------

    def get_laser_geometry(self):
        """
	read the geometry information of laser sensors.
	"""
	return self.laserGeometry

    def set_laser_config(self, min=-90.0, max=90.0, resolution=0.5, intensity=1):
        """
	change the configuration of laser sensors.
	"""
	pass
    
    def get_laser_config(self):
        """
	read the current configuration of laser sensors.
	"""
	return self.laserConfig

    #--------------------------------------------------------------------------
    # interfaces for the 'ptz' device.
    #--------------------------------------------------------------------------

    def set_ptz(self, pan, tilt, zoom):
        """
	move a camera.
	"""
	pan = pan * DEG2RAD
	tilt = tilt * DEG2RAD
	zoom = zoom * DEG2RAD
	try:
	    # send command
	    cmd = 'MISPKG {Type PanTilt} {Name %s} {Rotation 0,%f,%f}' % (self.ptzFrame,tilt,pan)
	    self.__sendline(cmd)
	    if self.debug: print '<sent a ptz command>'+ cmd
	    if zoom>0:
	        cmd = 'SET {Type Camera} {Name %s} {Opcode Zoom} {Params %f}' % (self.ptzName,zoom)
	        self.__sendline(cmd)
	        if self.debug: print '<sent a ptz command>'+ cmd

	except:
	    raise 'cannot send a ptz command'

    #--------------------------------------------------------------------------
    # interfaces for the 'bumper' device.
    #--------------------------------------------------------------------------

    def get_bumper_geometry(self):
        """
	read the geometry of bumper sensors.
	"""
	return self.bumperGeometry

    #--------------------------------------------------------------------------
    # interfaces for the 'truth' device.
    #--------------------------------------------------------------------------

    def get_truth_pose(self):
        """
	read the pose of truth sensors.
	"""
	return self.pose[0]

    #--------------------------------------------------------------------------
    # interfaces for the 'ptz' device.
    #--------------------------------------------------------------------------

    def release_tag(self):
        """
	release a RFID tag.
	"""
	try:
	    # send command
	    cmd = 'SET {Type RFIDReleaser} {Name %s} {Opcode Release}' % self.rfidReleaser
	    self.__sendline(cmd)
	    # NO RESPONSE
	    if self.debug: print '<release a RFID tag command>'+ cmd

	except:
	    raise 'cannot send set command'

    #--------------------------------------------------------------------------
    # utility functions for data retrieval.
    #--------------------------------------------------------------------------

    def get_power(self, index=0):
        """
	return the sensory value of a power device.
	"""
	return self.power[index]

    def get_pose(self, index=0):
        """
	return the sensory value of a position device.
	"""
	return self.pose[index]

    def get_rotation(self, index=0):
        """
	return the sensory value of a rotation device.
	"""
        return self.rotation[index]

    def get_velocity(self, index=0):
        """
	return the sensory value of a velocity device.
	"""
	return self.velocity[index]

    def get_sonar(self, index=0):
        """
	return the sensory value of a sonar device.
	"""
	return self.sonar[index]

    def get_laser(self, index=0):
        """
	return the sensory value of a laser device.
	"""
	return self.laser[index]

    def get_ptz(self, index=0):
        """
	return the sensory value of a ptz device.
	"""
	try:
	    res = self.ptz[index]
	except:
	    res = [0,0,0]
	return res

    def get_rfid(self, index=0):
        """
	return the RFID value detected by RFID reader.
	"""
	return self.rfid[index]

    def get_encoder(self, index=0):
        """
	return the tick value of a Encoder device.
	"""
	return self.encoder[index]

    def get_bumper(self, index=0):
        """
	return the bump value of a Bumper device.
	"""
	return self.bumper[index]

    def get_gps(self, index=0):
        """
	return the sensory value of a gps device.
	"""
	return self.gps[index]

    def get_truth(self, index=0):
        """
	return the sensory value of a truth device.
	"""
	return self.truth[index]


#---------------------------------------------------
#	UT Message
#---------------------------------------------------
class utmessage:
    def __init__(self, data):
        try:
            self.raw = data
            (self.head, self.body) = string.split(data, None, 1)
            self.segs = list()
            s = string.split(self.body, '}')
            for i in range(len(s)-1) :
                p = string.strip(s[i].replace('{', ''))
                ps = string.split(p)
                self.segs.append(dict())
                if len(ps)<2:
                    self.segs[0][ps[0]]=[]
                else:
                    for j in range(0,len(ps),2):
                        self.segs[i][ps[j]]=ps[j+1].split(',')
            self.segNum = len(s)
        except:
            print data
            raise

    def __repr__(self):
    	return "Message: " + self.head + " " + str(self.segs)

    #---------------------------------------------------------------
    #	Message paerser functions
    #---------------------------------------------------------------
    def getSegments(self):
    	return self.segs
    
    def getFirstValue(self, key):
    	"""
    	get the first value correspands to key
    	"""
    	for s in self.segs:
   	    if s.has_key(key):
    	        return s[key]
    	return ''
    
    def getValues(self, key):
    	"""
    	get all the values correspand to key
    	"""
    	res = list()
    	for s in self.segs:
            if s.has_key(key):
    	        res.append(s[key])
    	return res
    

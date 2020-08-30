import errno

def join(p):
    while True:
        try:
            p.join()
            return
        except OSError, ose:
            print "interrupt", ose
            if ose.errno != errno.EINTR:
                raise 
            

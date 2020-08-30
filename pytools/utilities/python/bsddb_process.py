from bsddb.db import DBLockDeadlockError, DBLockNotGrantedError, DBPageNotFoundError
import bsddb.dbshelve
import multiprocessing
import cPickle
from Queue import Empty
import process_utils
import atexit
import memcache
from memcache import Client
import traceback

def check_key(key, key_extra_len=0):
    """Checks sanity of key.  Fails if:
        Key length is > SERVER_MAX_KEY_LENGTH (Raises MemcachedKeyLength).
        Contains control characters  (Raises MemcachedKeyCharacterError).
        Is not a string (Raises MemcachedStringEncodingError)
        Is an unicode string (Raises MemcachedStringEncodingError)
        Is not a string (Raises MemcachedKeyError)
        Is None (Raises MemcachedKeyError)
    """
    if isinstance(key, tuple): key = key[1]
    if not key:
        raise Client.MemcachedKeyNoneError("Key is None: " + `key`)
    if isinstance(key, unicode):
        raise Client.MemcachedStringEncodingError(
                "Keys must be str()'s, not unicode.  Convert your unicode "
                "strings using mystring.encode(charset)!" + `key`)
    if not isinstance(key, str):
        raise Client.MemcachedKeyTypeError("Key must be str()'s" + `key`)

    if isinstance(key, basestring):
        for char in key:
            if ord(char) < 33 or ord(char) == 127:
                raise Client.MemcachedKeyCharacterError(
                        "Control characters not allowed" + `key` + " char: " + char)

def network_writer(queue):
    cache = memcache.Client(["127.0.0.1:21201"])
    while True:
        try:
            r = queue.get(block=True, timeout=0.5)
            if r == "terminate":
                return
            else:
                key, value = r
                cache.set(key, value)
        except Empty:
            pass


    
def file_writer(fname, queue):
    shelf = bsddb.dbshelve.open(fname, "c")
    while True:
        try:
            r = queue.get(block=True, timeout=0.5)
            if r == "terminate":
                print "closing"
                shelf.close()
                return
            else:

                key, value = r
                for i in range(0, 5):
                    try:
                        shelf[key] = value
                        shelf.sync()
                        break
                    except DBPageNotFoundError:
                        pass
                    

        except Empty:
            pass
    

dicts = []            

def terminator():
    """
    If we don't terminate the dictionary, the process hangs and never
    exits.  However this solution causes a memory leak.  It's a
    tradeoff.
    """
    for d in dicts:
        d.close()

atexit.register(terminator)


class Dict:
    
    def __init__(self, fname):
        self.fname = fname
        #self.shelf = bsddb.dbshelve.open(self.fname)
        self.cache = memcache.Client(["127.0.0.1:21201"])
        self.write_queue = multiprocessing.Queue()
        self.write_process = multiprocessing.Process(target=network_writer, 
                                                     args=(self.write_queue,))
        self.write_process.daemon = True
        self.write_process.start()

        dicts.append(self)
        
    def __setitem__(self, key, value):
        self.write_queue.put((key, value))

    def __getitem__(self, key):
        try:
            result = self.cache.get(key)
        except:
            print "except on key", key
            traceback.print_exc()
            raise KeyError()
        if result == None:
            raise KeyError()
        return result

    def disk_getitem__(self, key):
        try:
            return self.shelf[key]
        except DBPageNotFoundError:
            raise KeyError("Couldn't find key " + str(key))
        except cPickle.UnpicklingError:
            raise KeyError("Couldn't find key " + str(key))
        except EOFError:
            raise KeyError("Couldn't find key " + str(key))

    def close(self):
        print "bsddb_process sending close", self.write_queue.qsize()
        self.write_queue.put("terminate")
        print "bsddb_process joining"
        process_utils.join(self.write_process)
        print "bsddb_process done"
        

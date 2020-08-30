import hashlib
import lrudict
import os
#import pylibmc
import bsddb_process
import cPickle
import traceback

class Cache(object):
    """
    Memoize an object with a disk-based cache.  This uses pickle and
    can introduce subtle problems if keys, hash functions, or equals
    tests are incorrect.  It can also cause problems if the return
    value contains objects that are supposed to be pointers to other
    objects in the system; such links will be broken.
    """
    def __init__(self, fname, key_function, work_function):
        self.fname = fname
        self.key_function = key_function
        self.work_function = work_function
        self.lru_cache = lrudict.LruCache(cache_size=1000)

        self._open()
    def __del__(self):
        #self.close()
        pass
    def _close(self):
        if hasattr(self, "shelf"):
            self.shelf.close()
            #self.dbenv.close()
    def _open(self):
        # self.memcache = memcache.Client(["127.0.0.1:21201"])
        self.dict = bsddb_process.Dict(self.fname)
        self.pid = os.getpid()

    def close(self):
        self.dict.close()
        
    def hash_key(self, bigkey):
        m = hashlib.new("md4") # faster than md5
        m.update(bigkey)
        key = m.hexdigest()        
        return key

    def pr(self, string):
        print self.pid, string
    def cache(self, *args, **margs):
        key = self.key_function(*args, **margs)
        #key = self.hash_key(bigkey)
        # key = str(zlib.adler32(big_key))
        if key in self.lru_cache:
            return self.lru_cache[key]
        else:
            try:
                result = self.dict[key]
                try:
                    result = cPickle.loads(result)
                except:
                    self.pr("pickle: " + `result`)
                    raise KeyError()
            except KeyError:
                result = self.work_function(*args, **margs)
                self.dict[key] = cPickle.dumps(result)
            except:
                self.pr("except on key: " + `key`)
                raise
            self.lru_cache[key] = result
            return result

        

import hashlib

def fasthash(string):
    m = hashlib.new("md4") # faster than md5
    m.update(string)
    return m.hexdigest()

    

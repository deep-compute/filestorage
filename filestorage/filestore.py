import hashlib
import os
import gzip

class FileStore(object):
    def __init__(self, dirpath, compress=False):
        self.dirpath = dirpath
        self.compress = compress

    def _getid(self, key):
        return hashlib.md5(key).hexdigest()

    def _getpath(self, key):
        _id = self._getid(key)
        d1 = _id[0]
        d2 = _id[1]
        fname = _id[2:]
        dpath = os.path.join(self.dirpath, d1, d2)
        fpath = os.path.join(dpath, fname)
        return dpath, fpath

    def put(self, key, value):
        dpath, fpath = self._getpath(key)
        try:
            os.makedirs(dpath)
        except: pass

        if self.compress:
            gzip.open(fpath, 'wb').write(value)
        else:
            open(fpath, 'wb').write(value)

    def put_file(self, key, fpath):
        dpath, _fpath = self._getpath(key)
        os.makedirs(dpath)
        shutil.move(fpath, _fpath)

    def get(self, key):
        _, fpath = self._getpath(key)
        return open(fpath, 'rb').read()

    def get_file(self, key):
        _, fpath = self._getpath(key)
        return fpath

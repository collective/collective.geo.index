import os
import persistent
from BTrees import IOBTree
from rtree import Rtree

try:
    import zope.app.appsetup.product as zap
    INDEX_DIR = zap.getProductConfiguration('collective.geo.index')['directory']
except:
    INDEX_DIR = os.environ['CLIENT_HOME']

class BaseIndex(persistent.Persistent):

    def __init__(self):
        name = "rtree-%s" % hash(repr(self))
        self._basepath = os.path.sep.join([INDEX_DIR, name])
        self.clear()

    def clear(self):
        self.backward = IOBTree.IOBTree()
        try:
            os.unlink('%s.dat' % self._basepath)
            os.unlink('%s.idx' % self._basepath)
        except:
            pass

    @property
    def rtree(self):
        return Rtree(self._basepath)



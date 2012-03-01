import os
import persistent
from BTrees import IOBTree
from rtree import Rtree

import logging
logger = logging.getLogger('collective.geo.index')

INDEX_DIR = os.path.join(os.path.split(os.environ['CLIENT_HOME'])[0],
        'spatial-index')

if not os.path.exists(INDEX_DIR):
     os.mkdir(INDEX_DIR)


class BaseIndex(persistent.Persistent):

    def __init__(self):
        name = "rtree-%s" % hash(repr(self))
        self._basepath = os.path.sep.join([INDEX_DIR, name])
        self.clear()


    def numObjects(self):
        """Return the number of indexed objects."""
        return len(self.backward)

    def indexSize(self):
        """Return the size of the index """
        return 0
        if len(self.backward) > 1:
            try:
                if self.rtree:
                    return len(self.rtree.leaves())
            except:
                return
        else:
            return 0

    def clear(self):
        """ Complete reset """
        self.backward = IOBTree.IOBTree()
        try:
            os.unlink('%s.dat' % self._basepath)
            os.unlink('%s.idx' % self._basepath)
        except:
            pass

    def __nonzero__(self):
        return not not self.backward

    def items(self):
        items = []
        if len(self.backward) >0:
            for i,v,k in self.rtree.leaves():
                if isinstance(v, int):
                    v = IISet((v,))
                items.append((k, list(set(v))))
            return items


    @property
    def rtree(self):
        return Rtree(self._basepath)



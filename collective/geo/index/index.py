import os
import persistent
from BTrees import IOBTree
from rtree import Rtree
from zope.interface import alsoProvides
from interfaces import IGeometryCataloged

import logging
logger = logging.getLogger('collective.geo.index')

INDEX_DIR = os.path.join(os.path.split(os.environ['CLIENT_HOME'])[0],
        'spatial-index')

if not os.path.exists(INDEX_DIR):
     os.mkdir(INDEX_DIR)

#logger.info('Index directory: %s' % INDEX_DIR)


class BaseIndex(persistent.Persistent):

    def __init__(self):
        name = "rtree-%s" % hash(repr(self))
        self._basepath = os.path.sep.join([INDEX_DIR, name])
        self.clear()
        #logger.info('Index created: %s' % self._basepath )
        alsoProvides(self, IGeometryCataloged)


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



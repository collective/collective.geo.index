#
# Copyright (c) 2008 Eric BREHAULT
# contact: eric.brehault@makina-corpus.org
#
from App.special_dtml import DTMLFile
from OFS.SimpleItem import SimpleItem
from zope.interface import implements
from Products.PluginIndexes.common.util import parseIndexRequest
from Products.PluginIndexes.interfaces import IPluggableIndex
from Products.PluginIndexes.interfaces import ISortIndex
from Products.PluginIndexes.interfaces import IUniqueValueIndex
from shapely.geometry import MultiPoint

from BTrees.IIBTree import IITreeSet

from shapely import wkt
from index import BaseIndex

#from zgeo.wfs.interfaces import IWFSGeoItem
from collective.geo.contentlocations.interfaces import IGeoManager

import logging
logger = logging.getLogger('collective.geo.index')

def bboxAsTuple(geometry):
    """ return the geometry bbox as tuple
    """
    envelope=geometry.envelope
    if envelope.geometryType()=="Point":
        x=envelope.coords[0][0]
        y=envelope.coords[0][1]
        return (x,y,x,y)
    else:
        return envelope.bounds


class GeometryIndex(SimpleItem, BaseIndex):
    """Index for geometry attribute provided by IWFSGeoItem adapter
    """
    implements(IPluggableIndex, IUniqueValueIndex, ISortIndex)

    meta_type="GeometryIndex"

    query_options = ('query','geometry_operator')

    def __init__(self, id):
        self.id = id
        BaseIndex.__init__(self)
        self.clear()
        self.operators = ('equals', 'disjoint', 'intersects', 'touches', 'crosses', 'within', 'contains', 'overlaps')
        self.useOperator = 'within'

    def index_object(self, documentId, obj, threshold=None):
        """Index an object.

        'documentId' is the integer ID of the document.
        'obj' is the object to be indexed.
        """
        returnStatus = 0
        try:
            geoitem=IGeoManager(obj)
        except:
            return 0
        if geoitem.wkt:
            geometry = wkt.loads(geoitem.wkt)
        else:
            geometry = None
        if geoitem.isGeoreferenceable() and geoitem.getCoordinates()[1]:
            newValue = geoitem.wkt
            if newValue is callable:
                newValue = newValue()
            oldValue = self.backward.get(documentId, None )

            if newValue is None:
                if oldValue is not None:
                    self.rtree.delete(documentId, wkt.loads(oldValue).bounds)
                    try:
                        del self.backward[documentId]
                    except ConflictError:
                        raise
                    except:
                        pass
            else:
                if oldValue is not None and newValue!=oldValue:
                    self.rtree.delete(documentId, wkt.loads(oldValue).bounds)
                if geometry:
                    self.rtree.add(documentId, geometry.bounds)
                self.backward[documentId] = newValue

            returnStatus = 1

        return returnStatus

    def unindex_object( self, documentId ):
        """
            Remove the object corresponding to 'documentId' from the index.
        """
        datum = self.backward.get( documentId, None )

        if datum is None:
            return

        self.rtree.delete(documentId, wkt.loads(datum).bounds)
        del self.backward[ documentId ]

    def _apply_index(self, request, cid='', type=type):
        """
        """
        record = parseIndexRequest(request, self.id, self.query_options)
        if record.keys==None: return None
        r = None

        operator = record.get('geometry_operator',self.useOperator)
        if not operator in self.operators :
            raise RuntimeError,"operator not valid: %s" % operator
        if operator=='disjoint':
            raise RuntimeError,"DISJOINT not supported yet"


        # we only process one key
        key = record.keys[0]
        bbox = [float(c) for c in key.split(',')] #bboxAsTuple(key)
        intersection=self.rtree.intersection(bbox)
        set = []
        for d in [int(l) for l in intersection]:
            try:
                geom_wkt = self.backward.get( d, None )
            except:
                logger.debug('backward.get failed for %i' %d)
                continue
            if geom_wkt is not None:
                geom = wkt.loads(geom_wkt)
                if geom is not None:
                    opr=getattr(geom, operator)
                    mp = MultiPoint([bbox[:2],bbox[2:]])
                    if opr(mp.envelope):
                        set.append(d)

        r = IITreeSet(set)
        return r, (self.id,)

    def destroy_spatialindex(self):
        """
        """
        self.clear()


manage_addGeometryIndexForm = DTMLFile( 'dtml/addGeometryIndex', globals() )

def manage_addGeometryIndex( self, id, REQUEST=None, RESPONSE=None, URL3=None):
    """Add a DateDate index"""
    return self.manage_addIndex(id, 'GeometryIndex', extra=None, \
                    REQUEST=REQUEST, RESPONSE=RESPONSE, URL1=URL3)

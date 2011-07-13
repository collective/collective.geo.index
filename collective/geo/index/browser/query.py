#
from zope.interface import Interface, implements
from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from collective.geo.index.geometryindex import OPERATORS

from collective.geo.kml.interfaces import IKMLOpenLayersView

class ISearchView(Interface):
    """
    view interface
    """


class SearchView(BrowserView):

    implements(ISearchView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')


    def parse_bbox(self, bbox=None):
        if bbox is None:
            b = self.request.form.get('bbox')
        else:
            b = bbox
        return tuple(float(x) for x in b.split(','))




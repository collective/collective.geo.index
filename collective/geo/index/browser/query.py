#
from zope.interface import Interface, implements
from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from collective.geo.index.geometryindex import OPERATORS

class ISearchView(Interface):

    def num_items():
        """Number of items in index."""

    def searchResults(**searchterms):
        """Return iterator over results."""


class SearchView(BrowserView):

    implements(ISearchView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def num_items(self):
        """Number of items in index."""
        self.update()
        return len(self.index.backward)

    def parse_bbox(self, bbox=None):
        if bbox is None:
            b = self.request.form.get('bbox')
        else:
            b = bbox
        return tuple(float(x) for x in b.split(','))

    def searchResults(self, **searchterms):
        """Just like a catalog search."""
        self.update()
        return self.portal_catalog(**searchterms)


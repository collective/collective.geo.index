from zope.interface import implements, Interface
from plone.memoize import view
from Products.CMFCore.utils import getToolByName

from collective.geo.kml.browser.kmldocument import KMLBaseDocument, BrainPlacemark

from search import get_results

class IKmlView(Interface):
    """
    FlexiTopicKml view interface
    """


class KmlView(KMLBaseDocument):
    """
    FlexiTopicKml browser view
    """
    implements(IKmlView)


    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')


    @property
    @view.memoize
    def features(self):
        results = get_results(self.context, self.request)
        for brain in results:
            yield BrainPlacemark(brain, self.request, self)

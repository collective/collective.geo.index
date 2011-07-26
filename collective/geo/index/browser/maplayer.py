#
from collective.geo.mapwidget.browser.widget import MapLayers
from collective.geo.mapwidget.maplayers import MapLayer
from search import build_query
import ZTUtils

class KMLMapLayer(MapLayer):
    """
    a layer for one level sub objects.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def jsfactory(self):
        context_url = self.context.absolute_url()
        if not context_url.endswith('/'):
            context_url += '/'

        query, show = build_query(self.context, self.request)
        query_string = ZTUtils.make_query(query)
        return"""
        function() { return new OpenLayers.Layer.GML('%s', '%s' + '@@geometry_search.kml?%s',
            { format: OpenLayers.Format.KML,
              eventListeners: { 'loadend': function(event) {
                                     //Map zooms to bounding box rather
                                     //than results layer.
                                }
                            },
              projection: cgmap.createDefaultOptions().displayProjection,
              formatOptions: {
                  extractStyles: true,
                  extractAttributes: true }
            });}""" % ('search results',
                        context_url, query_string)


class KMLMapLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        layers = super(KMLMapLayers, self).layers()
        layers.append(KMLMapLayer(self.context, self.request))
        return layers

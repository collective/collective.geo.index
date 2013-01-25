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
        #return ''
        return u"""
        function() {
                return new OpenLayers.Layer.Vector("%s", {
                    protocol: new OpenLayers.Protocol.HTTP({
                      url: "%s@@geometry_search.kml?%s",
                      format: new OpenLayers.Format.KML({
                        extractStyles: true,
                        extractAttributes: true})
                      }),
                    strategies: [new OpenLayers.Strategy.Fixed()],
                    visibility: true,
                    projection: cgmap.createDefaultOptions().displayProjection
                  });
                } """ % (self.context.Title().replace("'", "&apos;"),
                        context_url, query_string)



class KMLMapLayers(MapLayers):
    '''
    create all layers for this view.
    '''

    def layers(self):
        layers = super(KMLMapLayers, self).layers()
        layers.append(KMLMapLayer(self.context, self.request))
        return layers

from zope.interface import implements
from zope.component.interfaces import ObjectEvent

from interfaces import IIndexableObjectWrapperEvent, ICatalogObjectEvent

class IndexableObjectWrapperEvent(ObjectEvent):
    implements(IIndexableObjectWrapperEvent)

    def __init__(self, object, index_name):
        ObjectEvent.__init__(self, object)
        self.index_name = index_name

class CatalogObjectEvent(ObjectEvent):
    implements(ICatalogObjectEvent)

    def __init__(self, object, catalog, indexes):
        ObjectEvent.__init__(self, object)
        self.catalog = catalog
        self.indexes = indexes


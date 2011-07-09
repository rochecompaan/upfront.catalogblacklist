from plone.indexer.interfaces import IIndexableObjectWrapper, IIndexableObject
from plone.indexer.wrapper import IndexableObjectWrapper as PloneWrapper

from Products.CMFCore.utils import getToolByName

class IndexableObjectWrapper(PloneWrapper):
    """ Specialise wrapper to not index values for blacklisted indexes
    """
    
    def __getattr__(self, name):
        idxs = set(self.__catalog.indexes())
        allowed_indexes = []

        if self.__catalog.id == 'portal_catalog':
            tool = getToolByName(self.__catalog,
                                 'portal_catalogblacklist', None)        
            if tool is not None:
                blacklisted = set(tool.getBlackListedIndexesForObject(
                    self.__object))
                allowed_indexes = idxs.difference(blacklisted)
           
                # we can only return if `name` is a catalog index since
                # not all attributes accessed match index names eg.
                # ZCatalog calls getPhysicalPath on the object since it
                # uses the path as uid
                if name in idxs and not name in allowed_indexes:
                    return

        return super(IndexableObjectWrapper, self).__getattr__(name)

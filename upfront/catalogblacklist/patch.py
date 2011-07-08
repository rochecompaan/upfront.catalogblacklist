from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.CatalogTool import CatalogTool

def catalog_object_wrapper(func):
    """ Filter indexes according to blacklist
    """

    def new(self, object, uid, idxs=None, update_metadata=1, pghandler=None):

        if idxs is None:
            idxs = self.indexes()

        idxs = set(idxs)
        allowed_indexes = []

        if self.id == 'portal_catalog':
            tool = getToolByName(self, 'portal_catalogblacklist', None)        
            if tool is not None:
                blacklisted = set(tool.getBlackListedIndexesForObject(object))
                allowed_indexes = idxs.difference(blacklisted)
           
                # Anything to do?
                if not allowed_indexes:
                    return

        return func(self, object, uid, idxs=list(allowed_indexes), 
            update_metadata=update_metadata, pghandler=pghandler
        )

    return new

CatalogTool.catalog_object = \
    catalog_object_wrapper(CatalogTool.catalog_object)



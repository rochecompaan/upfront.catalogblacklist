from types import StringTypes

from App.class_init import InitializeClass
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo
from ComputedAttribute import ComputedAttribute

from persistent.dict import PersistentDict
from zope.interface import implements
from zope.dottedname.resolve import resolve

from Products.CMFCore.utils import UniqueObject, registerToolInterface, \
    getToolByName

from interfaces import ICatalogBlacklist

class CatalogBlacklist(UniqueObject, SimpleItem):

    implements(ICatalogBlacklist)

    id = 'portal_catalogblacklist'
    meta_type = 'Catalog Blacklist Tool'

    security = ClassSecurityInfo()

    def __init__(self, id=None):
        self._blacklisted_types = PersistentDict()
        self._blacklisted_interfaces = PersistentDict()

    security.declarePrivate('extend')
    def extend(self, blacklisted_types=None, blacklisted_interfaces=None):
        """ extend the blacklisted indexes for the given types or
            interfaces
        """
        if blacklisted_types is not None:
            for pt, indexnames in blacklisted_types.items():
                self._blacklisted_types.setdefault(pt, [])
                for name in indexnames:
                    if name not in self._blacklisted_types[pt]:
                        self._blacklisted_types[pt].append(name)
            self._blacklisted_types._p_changed = 1

        if blacklisted_interfaces is not None:
            for iface, indexnames in blacklisted_interfaces.items():
                if isinstance(iface, StringTypes):
                    iface = resolve(iface)
                self._blacklisted_interfaces.setdefault(iface, [])
                for name in indexnames:
                    if name not in self._blacklisted_interfaces[iface]:
                        self._blacklisted_interfaces[iface].append(name)
            self._blacklisted_interfaces._p_changed = 1

    security.declarePrivate('getBlackListedIndexesForObject')
    def getBlackListedIndexesForObject(self, object):
        """ return blacklisted indexes for object
        """
        portal_type = getattr(object, 'portal_type', None)
        blacklisted = []
        for indexname in self._blacklisted_types.get(portal_type, []):
            blacklisted.append(indexname)

        # Inspect the interfaces
        for iface, indexes in \
                self._blacklisted_interfaces.items():                
            if iface.providedBy(object):
                for indexname in indexes:
                    if indexname not in blacklisted:
                        blacklisted.append(indexname)

        return blacklisted


InitializeClass(CatalogBlacklist)
registerToolInterface('portal_catalogblacklist', ICatalogBlacklist)

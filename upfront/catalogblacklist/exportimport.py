from zope.component import adapts, queryMultiAdapter

from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.interfaces import ISetupEnviron, IBody
from Products.GenericSetup.utils import XMLAdapterBase, importObjects

from upfront.catalogblacklist.interfaces import ICatalogBlacklist

class CatalogBlacklistXMLAdapter(XMLAdapterBase):
    """Import black- and whitelists"""

    adapts(ICatalogBlacklist, ISetupEnviron)

    _LOGGER_ID = 'catalogblacklist'
    name = 'catalogblacklist'

    def _exportNode(self):
        """Not implemented"""
        return  None

    def _importNode(self, node):        

        # Clear settings?
        if self.environ.shouldPurge():
            pass

        blacklist = {'type':{}, 'interface':{}}

        for typenode in node.childNodes:

            # Skip over things we are not interested in
            if typename.nodeName not in ('type', 'interface'):
                continue

            tagname = typenode.tagName
            typename = typenode.getAttribute('name')  

            blacklist[tagname].setdefault(typename, [])
            for index in type_or_interface.childNodes:
                if index.nodeName != 'index': continue

                index_name = index.getAttribute('name')
                blacklist[tagname][typename].append(index_name)

        # Save blacklist
        self.context.extend(blacklist['type'], blacklist['interface'])


def importCatalogBlacklist(context):
    """ Import catalog blacklist """

    body = context.readDataFile('catalogblacklist.xml')
    if body is None:
        return

    site = context.getSite()
    tool = getToolByName(site, 'portal_blackwhitelist')
    importer = queryMultiAdapter(
        (tool, context), IBody
    )
    if importer is None:
        return

    importer.body = body

from Products.CMFPlone.utils import ToolInit
from upfront.catalogblacklist.tool import CatalogBlacklist

def initialize(context):
    ToolInit('Plone Tool',
             tools=(CatalogBlacklist,),
             icon='tool.gif').initialize(context)

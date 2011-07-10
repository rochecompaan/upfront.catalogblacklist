#
# CatalogBlacklist GS profile tests
#

import unittest
import zope.interface

from Testing import ZopeTestCase
from Products.CMFPlone.tests import PloneTestCase
from Products.GenericSetup.tests.common import DummyImportContext

from upfront.catalogblacklist.exportimport import importCatalogBlacklist
from upfront.catalogblacklist.exportimport import CATALOGBLACKLIST_XML
from upfront.catalogblacklist.exportimport import CatalogBlacklistXMLAdapter

ZopeTestCase.installProduct('upfront.catalogblacklist', quiet=1)

_TEST1_XML = """\
<?xml version="1.0"?>
<blacklist>
    <type name="Document">
        <index name="object_provides" />
        <index name="Description" />
    </type>
    <type name="Folder">
        <index name="object_provides" />
    </type>
    <type name="Event">
        <index name="*" />
    </type>
    <interface name="Products.ATContentTypes.interfaces.IATFolder">
        <index name="object_provides" />
    </interface>
</blacklist>
"""

class TestExportImport(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.addProfile('upfront.catalogblacklist:default')
        self.catalogblacklist = self.portal.portal_catalogblacklist
        self.folder.invokeFactory('Document', id='doc',
            title='Foo', description='Bar')
        self.folder.invokeFactory('Event', id='event',
            title='Foo', description='Bar')

    def test_importNode(self):
        context = DummyImportContext(self.portal, self.portal.portal_setup)
        context._files[ CATALOGBLACKLIST_XML ] = _TEST1_XML

        xmladapter = CatalogBlacklistXMLAdapter(self.catalogblacklist, context)
        xmladapter._importBody(_TEST1_XML)

        self.assertEqual(
            self.catalogblacklist.getBlackListedIndexesForObject(
                self.folder.doc),
            [u'object_provides', u'Description'])
        self.assertEqual(
            self.catalogblacklist.getBlackListedIndexesForObject(
                self.folder),
            [u'object_provides'])

    def test_importCatalogBlacklist(self):
        context = DummyImportContext(self.portal, self.portal.portal_setup)
        context._files[ CATALOGBLACKLIST_XML ] = _TEST1_XML

        self.assertEqual(
            self.catalogblacklist.getBlackListedIndexesForObject(
                self.folder.doc),
            [u'object_provides', u'Description'])
        self.assertEqual(
            self.catalogblacklist.getBlackListedIndexesForObject(
                self.folder),
            [u'object_provides'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestExportImport))
    return suite

#
# IndexableObjectWrapper tests
#

import unittest
import zope.interface
from zope.component import queryMultiAdapter

from Testing import ZopeTestCase
from Products.CMFPlone.tests import PloneTestCase

from plone.indexer.interfaces import IIndexableObject
from upfront.catalogblacklist.wrapper import IndexableObjectWrapper

ZopeTestCase.installProduct('upfront.catalogblacklist', quiet=1)

class TestIndexableObjectWrapper(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.addProfile('upfront.catalogblacklist:default')
        self.catalog = self.portal.portal_catalog
        self.catalogblacklist = self.portal.portal_catalogblacklist

        # blacklist all indexes except SearchableText, Title and
        # review_state
        blacklist = self.catalog.indexes()
        blacklist.remove('SearchableText')
        blacklist.remove('Title')
        blacklist.remove('review_state')

        self.catalogblacklist.extend(blacklisted_types={
            'Document': blacklist
            }
        )
        self.folder.invokeFactory('Document', id='doc',
            title='Foo', description='Bar')
        self.catalog.unindexObject(self.folder.doc)


    def test_component_lookup(self):
        """ Test our override - a lookup should yield our own wrapper,
            not Plone's default wrapper.
        """
        wrapper = queryMultiAdapter((self.folder.doc,
                                     self.portal.portal_catalog),
                                    IIndexableObject)
        self.assertEqual(
            wrapper.__class__,
            IndexableObjectWrapper)

    def test_getattr(self):
        wrapper = queryMultiAdapter((self.folder.doc,
                                     self.portal.portal_catalog),
                                    IIndexableObject)
        self.assertEqual(wrapper.Description, None)
        self.assertEqual(wrapper.Title(), 'Foo')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestIndexableObjectWrapper))
    return suite

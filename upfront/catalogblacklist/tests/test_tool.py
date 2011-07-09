#
# CatalogBlacklist Tool tests
#

import unittest
import zope.interface

from Testing import ZopeTestCase
from Products.CMFPlone.tests import PloneTestCase

ZopeTestCase.installProduct('upfront.catalogblacklist', quiet=1)

class TestCatalogBlacklist(PloneTestCase.PloneTestCase):

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

    def assertResults(self, result, expect):
        # Verifies ids of catalog results against expected ids
        lhs = [r.getId for r in result]
        lhs.sort()
        rhs = list(expect)
        rhs.sort()
        self.assertEqual(lhs, rhs)

    def test_getBlackListedIndexesForObject(self):
        blacklist = self.catalog.indexes()
        blacklist.remove('SearchableText')
        blacklist.remove('Title')
        blacklist.remove('review_state')

        self.assertEqual(
            self.catalogblacklist.getBlackListedIndexesForObject(
                self.folder.doc),
            blacklist)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCatalogBlacklist))
    return suite

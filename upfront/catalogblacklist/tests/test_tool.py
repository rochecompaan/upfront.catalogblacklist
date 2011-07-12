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
        self.catalog.manage_catalogClear()
        self.folder.invokeFactory('Document', id='doc',
            title='Doc', description='Doc')

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

    def test_searchOnBlacklistIndexes(self):
        self.assertResults(self.catalog(), [])
        self.assertResults(self.catalog(portal_type='Document'), [])
        self.assertResults(self.catalog(id='doc'), [])
        self.assertResults(self.catalog(SearchableText='Doc'), ['doc'])
        self.assertResults(self.catalog(Title='Doc'), ['doc'])
        self.assertResults(self.catalog(review_state='private'), ['doc'])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCatalogBlacklist))
    return suite

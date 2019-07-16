# -*- coding:utf-8 -*-
import unittest

from bluelog.models import Admin, Post, Category, Comment, Link
from tests.base import BaseTestCase


class CLITestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_init_db_command(self):
        result = self.runner.invoke(args=['init-db'])
        self.assertIn('Initialized database.', result.output)

    def test_forge_new_command(self):
        result = self.runner.invoke(args=['forge-new'])

        self.assertEqual(Admin.query.count(), 1)
        self.assertIn('Generating the administrator...', result.output)

        self.assertEqual(Post.query.count(), 50)
        self.assertIn('Generating 50 posts...', result.output)

        self.assertEqual(Category.query.count(), 11)
        self.assertIn('Generating 10 categories...', result.output)

        self.assertEqual(Comment.query.count(), 650)
        self.assertIn('Generating 500 comments...', result.output)

        self.assertEqual(Link.query.count(), 4)
        self.assertIn('Generating links...', result.output)
        self.assertIn('Done.', result.output)


if __name__ == '__main__':
    unittest.main()

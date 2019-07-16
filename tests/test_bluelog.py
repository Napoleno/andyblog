# -*- coding:utf-8 -*-
import datetime
import unittest

from bluelog import db
from wsgi import app


class TestBluelog(unittest.TestCase):

    def setUp(self):
        app.config.update(
            dict(TESTING=True,
                 SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
        )
        db.create_all()
        self.runner = app.test_cli_runner()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_location_by_model(self):
        '这个测试类报错： No application found. Either work inside a view function or push an application context'
        # self.runner.invoke(get_location_by_model)
        result = self.runner.invoke(args=['get_location_by_model'])
        self.assertIn('Xiaomi', result.output)

    def test_datetime(self):
        d = datetime.datetime.utcnow()
        print(d)


if __name__ == '__main__':
    unittest.main()

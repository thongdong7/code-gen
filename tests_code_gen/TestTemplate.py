# encoding=utf-8
import logging
import unittest

from code_gen.model.template import Template
from tests_code_gen.bootstrap import get_test_dir

__author__ = 'hiepsimu'

logging.basicConfig(level=logging.DEBUG)


class TemplateTestCase(unittest.TestCase):
    def test_01(self):
        d = get_test_dir('test01_template')
        t = Template(d)
        self.assertEqual(3, len(t.config.override))
        self.assertIn('a', t.parameters)
        self.assertIn('b', t.parameters)


if __name__ == '__main__':
    unittest.main()

# encoding=utf-8
import logging
import unittest
from pprint import pprint

from code_gen.model.template import Template
from code_gen.provider.template import TemplateProvider
from tests_code_gen.bootstrap import get_test_dir

__author__ = 'hiepsimu'

logging.basicConfig(level=logging.DEBUG)


class TemplateTestCase(unittest.TestCase):
    def test_01(self):
        d = get_test_dir('test01_template/.code-gen/t1')
        t = Template(d)
        self.assertEqual(3, len(t.config.override))
        self.assertIn('a', t.parameters)
        self.assertIn('b', t.parameters)

    def test_02_merge(self):
        d1 = get_test_dir('test01_template/.code-gen/t1')
        d2 = get_test_dir('test01_template/.code-gen/t2')
        t1 = Template(d1)
        t2 = Template(d2)

        t1.merge(t2)
        # pprint(t1.config.override)
        self.assertEqual(6, len(t1.config.override))

        self.assertIn('file1', t1.config.override)

        # Parameters are merged. `t2` will override `t1`
        self.assertEqual(2, t1.parameters['a'])
        self.assertEqual(2, t1.parameters['b'])
        self.assertEqual(3, t1.parameters['c'])

        self.assertEqual(2, len(t1.paths))
        # print(t1.path)

    def test_03_template_provider(self):
        d = get_test_dir('test01_template')
        template_provider = TemplateProvider()
        t = template_provider.get(d)

        self.assertEqual(6, len(t.config.override))
        self.assertEqual(2, t.parameters['a'])
        self.assertEqual(2, len(t.paths))


if __name__ == '__main__':
    unittest.main()

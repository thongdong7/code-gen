from os import makedirs
from os.path import exists, join

from code_gen.generator import CodeGenerator
from code_gen.utils import io_utils
from tests_code_gen.bootstrap import get_test_dir

__author__ = 'johnsmith'
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)


class GeneratorTestCase(unittest.TestCase):
    def test_01(self):
        d = get_test_dir('test01_template')
        output_dir = '/tmp/test-code-gen'
        if not exists(output_dir):
            makedirs(output_dir)

        generator = CodeGenerator(d, output_dir)
        generator.generate()

        ab_content = io_utils.get_content(join(output_dir, 'ab.txt'))
        # print(content)
        self.assertEqual('a is 2. b is 2', ab_content)

        abc_content = io_utils.get_content(join(output_dir, 'abc.txt'))
        # print(content)
        self.assertEqual('a is 2. b is 2. c is 3', abc_content)


if __name__ == '__main__':
    unittest.main()

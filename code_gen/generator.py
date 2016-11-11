# encoding=utf-8
from os.path import join, exists, abspath

from code_gen.monitor import FileMonitor, FileMonitorPool
from code_gen.provider.template import TemplateProvider
from code_gen.renderer import Renderer
from code_gen.utils.template_utils import generate
from tornado.gen import sleep


class CodeGenerator(object):
    def __init__(self, path, output_dir):
        self.path = abspath(path)
        self.template = TemplateProvider().get(path)
        self.output_dir = output_dir

        #
        self.renderer = Renderer()

    def generate(self, watch=False):
        self._generate()

        if watch:
            file_monitor = FileMonitor(self._on_change)
            print('Watch folders', self.template.paths)
            file_monitor.watch_multiple(self.template.paths)

            pool = FileMonitorPool()
            pool.add_file_monitor(file_monitor)
            pool.start()

            while True:
                sleep(1000)

    def _on_change(self, path):
        print('%s changed' % path)
        self._generate()

    def _generate(self):
        print('Generating...')
        # Reload parameters
        self.template = TemplateProvider().get(self.path)

        # TODO Check changed path to decide to reload parameters or not
        params = self.template.parameters

        # Generate master
        self._generate_master(params)

        # TODO Generate items
        print('Done!')

    def _generate_master(self, params):
        for path in self.template.paths:
            print('  > %s' % path)
            template_dir = join(path, 'master')
            if not exists(template_dir):
                continue

            generate(template_dir=template_dir, params=params, output_dir=self.output_dir,
                     override=self.template.config.override)

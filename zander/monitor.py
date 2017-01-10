# encoding=utf-8

import os
from os import walk
from os.path import abspath, isdir, join

from tornado.ioloop import IOLoop, PeriodicCallback


class FileChange(Exception):
    def __init__(self, path, *args, **kwargs):
        super(FileChange, self).__init__(path, *args, **kwargs)
        self.path = path


class FileMonitor:
    def __init__(self, callback):
        self.callback = callback
        self.watched_files = set()
        self.modify_times = {}
        self.root_path_map = {}

    def watch(self, path):
        self.watched_files.add(path)

    def watch_multiple(self, paths):
        for path in paths:
            self._add(path)

    def _add(self, path):
        if not isdir(path):
            full_path = abspath(path)
            self.root_path_map[full_path] = path
            self.watched_files.add(full_path)
        else:
            f = []
            for (dirpath, dirnames, filenames) in walk(path):
                for filename in filenames:
                    f.append(join(dirpath, filename))
                # f.extend(filenames)
            # print f

            for item in f:
                full_path = abspath(item)
                self.root_path_map[full_path] = path
                self.watched_files.add(full_path)

    def scan(self):
        try:
            for path in self.watched_files:
                self.check_file(path)
        except FileChange as e:
            self.callback(e.path)

    def check_file(self, path):
        try:
            modified = os.stat(path).st_mtime
        except Exception:
            return

        if path not in self.modify_times:
            self.modify_times[path] = modified
            return
        if self.modify_times[path] != modified:
            self.modify_times[path] = modified

            actual_path = self.root_path_map[path]
            raise FileChange(actual_path)


class FileMonitorPool:
    def __init__(self):
        self.io_loop = IOLoop.instance()
        self.file_monitors = []

    def add_file_monitor(self, file_monitor):
        self.file_monitors.append(file_monitor)

    def start(self, check_time=500):
        scheduler = PeriodicCallback(self._callback, check_time, io_loop=self.io_loop)
        scheduler.start()

        self.io_loop.start()

    def _callback(self):
        for file_monitor in self.file_monitors:
            file_monitor.scan()

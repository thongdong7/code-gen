# encoding=utf-8
import os

from os.path import join

current_folder = os.path.abspath(os.path.dirname(__file__))
data_folder = join(current_folder, 'data')


def get_data_dir(name):
    return join(data_folder, name)

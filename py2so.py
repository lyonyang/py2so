#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = Lyon

"""
>>> python py2so.py -i py2so.py -d dist -v 3
"""

import os
import time
import shutil
import argparse
from distutils.core import setup
from Cython.Build import cythonize

ROOT_PATH = os.path.abspath('.')
PROJECT_NAME = ROOT_PATH.split('/')[-1]

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--ignore', default=[], nargs='+', help='ignore files for compile.')
parser.add_argument('-d', '--dir', default='dist', help='result directory.')
parser.add_argument('-v', '--version', default=3, help='python version.')
parser.add_argument('-c', '--copy_py', default=[], nargs='+', help='copy py files.')
args = parser.parse_args()

args.ignore.append('py2so.py')


def ls(dir=''):
    """Return all relative path under the current folder."""
    dir_path = os.path.join(ROOT_PATH, dir)
    for filename in os.listdir(dir_path):
        absolute_file_path = os.path.join(dir_path, filename)
        file_path = os.path.join(dir, filename)
        if filename.startswith('.'):
            continue
        if os.path.isdir(absolute_file_path) and not filename.startswith('__'):
            for file in ls(file_path):
                yield file
        else:
            yield file_path


def copy_ignore():
    """Copy ignore files"""
    files = ls()
    for file in files:
        file_arr = file.split('/')
        if file_arr[0] == args.dir:
            continue
        suffix = os.path.splitext(file)[1]
        if not suffix:
            continue
        if file_arr[0] not in args.copy_py and file not in args.copy_py:
            if suffix in ('.pyc', '.pyx'):
                continue
            elif suffix == '.py':
                continue
        src = os.path.join(ROOT_PATH, file)
        dst = os.path.join(ROOT_PATH, os.path.join(args.dir, file.replace(ROOT_PATH, '', 1)))
        dir = '/'.join(dst.split('/')[:-1])
        if not os.path.exists(dir):
            os.makedirs(dir)
        shutil.copyfile(src, dst)


def build():
    """py -> c -> so"""
    start = time.time()
    files = list(ls())
    module_list = list()
    for file in files:
        suffix = os.path.splitext(file)[1]
        if not suffix:
            continue
        elif file.split('/')[0] in args.ignore or file in args.ignore:
            continue
        elif suffix in ('.pyc', '.pyx'):
            continue
        elif suffix == '.py':
            module_list.append(file)

    dist_temp = os.path.join(os.path.join('.', args.dir), 'temp')
    try:
        setup(ext_modules=cythonize(module_list, compiler_directives={'language_level': args.version}),
              script_args=["build_ext", "-b", os.path.join('.', args.dir), "-t", dist_temp])
    except Exception as e:
        print('Error: ', e)
        if os.path.exists(dist_temp):
            shutil.rmtree(dist_temp)
        for file in ls():
            if not file.endswith('.c'):
                continue
            os.remove(os.path.join(ROOT_PATH, file))
        return

    if os.path.exists(dist_temp):
        shutil.rmtree(dist_temp)
    for file in ls():
        if not file.endswith('.c'):
            continue
        os.remove(os.path.join(ROOT_PATH, file))

    copy_ignore()
    end = time.time()
    print('Complete, %.2fs !' % (end - start))


if __name__ == '__main__':
    build()

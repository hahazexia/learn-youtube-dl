#!/usr/bin/env python
# coding: utf-8

# 在开头加上 from __future__ import print_function 这句之后，即使在 python2.X，使用 print 就得像 python3.X 那样加括号使用。python2.X 中 print不需要括号，而在 python3.X 中则需要
from __future__ import print_function

# os.path 常用路径操作
# warnings 警报相关方法
# sys 系统相关方法
import os.path
import warnings
import sys

# 尝试使用 setuptools 分发工具，如果引入失败则引入 python 自带标准库分发工具 distutils。并设置 setuptools_available 标志是否 setuptools 可用
try:
    from setuptools import setup, Command
    setuptools_available = True
except ImportError:
    from distutils.core import setup, Command
    setuptools_available = False
# spawn 在子进程中启动程序
from distutils.spawn import spawn

# 尝试引入 py2exe 这是一个将 python 脚本转换成 windows exe 的工具
try:
    # This will create an exe that needs Microsoft Visual C++ 2008
    # Redistributable Package
    import py2exe
except ImportError:
    if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
        print('Cannot import py2exe', file=sys.stderr)
        exit(1)

py2exe_options = {
    'bundle_files': 1,
    'compressed': 1,
    'optimize': 2,
    'dist_dir': '.',
    'dll_excludes': ['w9xpopen.exe', 'crypt32.dll'],
}

# Get the version from youtube_dl/version.py without importing the package
exec(compile(open('youtube_dl/version.py').read(),
             'youtube_dl/version.py', 'exec'))

DESCRIPTION = 'YouTube video downloader'
LONG_DESCRIPTION = 'Command-line program to download videos from YouTube.com and other video sites'

py2exe_console = [{
    'script': './youtube_dl/__main__.py',
    'dest_base': 'youtube-dl',
    'version': __version__,
    'description': DESCRIPTION,
    'comments': LONG_DESCRIPTION,
    'product_name': 'youtube-dl',
    'product_version': __version__,
}]

py2exe_params = {
    'console': py2exe_console,
    'options': {'py2exe': py2exe_options},
    'zipfile': None
}

if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
    params = py2exe_params
else:
    files_spec = [
        ('etc/bash_completion.d', ['youtube-dl.bash-completion']),
        ('etc/fish/completions', ['youtube-dl.fish']),
        ('share/doc/youtube_dl', ['README.txt']),
        ('share/man/man1', ['youtube-dl.1'])
    ]
    root = os.path.dirname(os.path.abspath(__file__))
    data_files = []
    for dirname, files in files_spec:
        resfiles = []
        for fn in files:
            if not os.path.exists(fn):
                warnings.warn('Skipping file %s since it is not present. Type  make  to build all automatically generated files.' % fn)
            else:
                resfiles.append(fn)
        data_files.append((dirname, resfiles))

    params = {
        'data_files': data_files,
    }
    if setuptools_available:
        params['entry_points'] = {'console_scripts': ['youtube-dl = youtube_dl:main']}
    else:
        params['scripts'] = ['bin/youtube-dl']

class build_lazy_extractors(Command):
    description = 'Build the extractor lazy loading module'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        spawn(
            [sys.executable, 'devscripts/make_lazy_extractors.py', 'youtube_dl/extractor/lazy_extractors.py'],
            dry_run=self.dry_run,
        )

setup(
    name='youtube_dl',
    version=__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://github.com/ytdl-org/youtube-dl',
    author='Ricardo Garcia',
    author_email='ytdl@yt-dl.org',
    maintainer='Sergey M.',
    maintainer_email='dstftw@gmail.com',
    license='Unlicense',
    packages=[
        'youtube_dl',
        'youtube_dl.extractor', 'youtube_dl.downloader',
        'youtube_dl.postprocessor'],

    # Provokes warning on most systems (why?!)
    # test_suite = 'nose.collector',
    # test_requires = ['nosetest'],

    classifiers=[
        'Topic :: Multimedia :: Video',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: IronPython',
        'Programming Language :: Python :: Implementation :: Jython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    cmdclass={'build_lazy_extractors': build_lazy_extractors},
    **params
)

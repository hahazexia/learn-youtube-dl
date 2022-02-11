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

# py2exe 会扩展 distutils 从而产生新的命令，在 setup.py 文件中引入 py2exe 后会添加新命令
# 下面是一些 setup 方法参数 options.py2exe 中的参数
    # bundle_files 将 dll 文件打包成 zip 文件或者 exe 文件。合法值： 3 = 不打包（默认值） 2 = 打包所有文件除了 python 解释器 1 = 打包所有文件包含 python 解释器
    # compressed 布尔值 是否创建一个压缩 zip 文件
    # optimize 字符串或整数，表示优化级别（0 1 或 2）0 = 不做优化（生成 .pyc 文件）1 = 普通优化（类似于 python -O）2 = 额外优化（类似 python -OO）查看 http://docs.python.org/distutils/apiref.html#module-distutils.util 更多信息
    # dist_dir 最终文件输出的目录
    # dll_excludes 需要排除在外的 dll 组成的 list

# setup 方法参数 options.py2exe 参数
py2exe_options = {
    'bundle_files': 1, # 打包所有文件，包括 python 解释器
    'compressed': 1, # 创建压缩 zip 文件
    'optimize': 2, # 做最大额外优化
    'dist_dir': '.', # 输出目录
    'dll_excludes': ['w9xpopen.exe', 'crypt32.dll'], # 打包排除的文件组成的 list
}

# Get the version from youtube_dl/version.py without importing the package
# open 内置函数，打开 file 并返回对应的 file object。fileObject.read() 读取整个文件
# compile 内置函数，将字符串编译成代码对象，代码对象可以被 exec 或者 eval 执行

# 通过 youtube_dl/version.py 代码文件获取到版本号，而不需要引入整个包
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

# console 需要转换成 控制台 exe 的脚本组成的 list
# zipfile 生成的可分享的 zip 文件的名字；允许指定一个子目录；默认值是 library.zip。如果 zipfile 设置为 None，那么文件将会被打包到可执行文件中

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

# https://setuptools.pypa.io/en/latest/references/keywords.html setuptools 官网文档
setup(
    name='youtube_dl', # 包名
    version=__version__, # 版本号
    description=DESCRIPTION, # 简单描述
    long_description=LONG_DESCRIPTION, # 详细描述
    url='https://github.com/ytdl-org/youtube-dl', # 官网地址
    author='Ricardo Garcia', # 作者
    author_email='ytdl@yt-dl.org', # 作者邮箱
    maintainer='Sergey M.', # 维护者
    maintainer_email='dstftw@gmail.com', # 维护者邮箱
    license='Unlicense', # 许可证
    packages=[
        'youtube_dl',
        'youtube_dl.extractor', 'youtube_dl.downloader',
        'youtube_dl.postprocessor'], # 需要处理的包目录(通常为包含 __init__.py 的文件夹)

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

    cmdclass={'build_lazy_extractors': build_lazy_extractors}, # 自定义命令的别名 map 表
    **params
)

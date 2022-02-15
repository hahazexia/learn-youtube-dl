#!/usr/bin/env python

# Python 中有些库的接口要求参数必须是 str 类型字符串，有些接口要求参数必须是 unicode 类型字符串。对于 str 类型的字符串，调用 len()和遍历时，其实都是以字节为单位的，同一个字符使用不同的编码格式，长度往往是不同的。对 unicode 类型的字符串调用 len() 和遍历才是以字符为单位，这是我们所要的。另外，Django，Django REST framework 的接口都是返回 unicode 类型的字符串。为了统一，我个人建议使用 from __future__ import unicode_literals，将模块中显式出现的所有字符串转为 unicode 类型
from __future__ import unicode_literals

# Execute with
# $ python youtube_dl/__main__.py (2.6+)
# $ python -m youtube_dl          (2.7+)

import sys

if __package__ is None and not hasattr(sys, 'frozen'):
    # direct call of __main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import youtube_dl

# __name__ 是每一个模块解析时生成的，代表这个模块的名字。如果 __name__ 和 '__main__' 相等，则说明当前模块是被直接运行的，而不是被导入其他模块中再运行。因此这个判断逻辑的后面就是当前模块直接运行时才会执行的代码
# 当模块被导入其他模块中运行时，其 __name__ 值就是模块的真实名称，比如 package.A
if __name__ == '__main__':
    youtube_dl.main()

# 对于 python -m youtube-dl 的调用模式，__init__.py 先被载入，此时 python 解释器已经知道自己是一个 package，因此将当前路径加入到 sys.path 中，然后再去执行 __main__py
# 而对于 python youtube-dl 的调用模式，__init__.py 不被载入，这时候 python 解释器将 __main__.py 的路径加入到 sys.path 中，然后在这个路径下去找这个模块，因此会报错找不到

# 因此想要 python -m youtube-dl 或者 python youtube-dl 的模式都可以运行，就要将当前路径加入到 sys.path 中
# 这也是上面那段代码的作用，可以让 python youtube-dl 命令也就是直接运行 __main__.py 起作用

'''
if __package__ is None and not hasattr(sys, 'frozen'):
    # direct call of __main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))
'''

# 如果一个模块或者代码以文件名运行，这时候 __package__ 为 None

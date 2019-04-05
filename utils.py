from __future__ import unicode_literals

import inspect
import time


def custom_time(timestamp):
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt


def embed(local=None, banner='', shell=None):
    """
    | 进入交互式的 Python 命令行界面，并堵塞当前线程
    | 支持使用 ipython, bpython 以及原生 python
    :param str shell:
        | 指定命令行类型，可设为 'ipython'，'bpython'，'python'，或它们的首字母；
        | 若为 `None`，则按上述优先级进入首个可用的 Python 命令行。
    :param dict local: 设定本地变量环境，若为 `None`，则获取进入之前的变量环境。
    :param str banner: 设定欢迎内容，将在进入命令行后展示。
    """

    import inspect

    if not local:
        local = inspect.currentframe().f_back.f_locals

    if isinstance(shell, str):
        shell = shell.strip().lower()
        if shell.startswith('b'):
            shell = _bpython
        elif shell.startswith('i'):
            shell = _ipython
        elif shell.startswith('p') or not shell:
            shell = _python

    for _shell in shell, _ipython, _bpython, _python:
        try:
            _shell(local=local, banner=banner)
        except (TypeError, ImportError):
            continue
        except KeyboardInterrupt:
            break
        else:
            break
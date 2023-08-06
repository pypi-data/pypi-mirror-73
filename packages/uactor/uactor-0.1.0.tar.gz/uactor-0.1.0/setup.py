"""
uActor setuptools script.

uActor multiprocessing microframework.

See README.md provided in source distributions or available
at the `project repository <https://gitlab.com/ergoithz/uactor>`_.

Copyright (c) 2020, Felipe A Hernandez
MIT License (see LICENSE)

"""

import io
import re

from setuptools import setup


repository = 'https://gitlab.com/ergoithz/uactor'


with io.open('README.md', 'rt', encoding='utf8') as f:
    content = f.read()
    readme = re.sub(
        r'(?P<prefix>!?)\[(?P<text>[^]]+)\]\(\./(?P<src>[^)]+)\)',
        lambda match: (
            '{prefix}[{text}]({repository}/-/{view}/master/{src})'.format(
                repository=repository,
                view='raw' if match.group('prefix') == '!' else 'blob',
                **match.groupdict(),
                )),
        content,
        )


with io.open('uactor.py', 'rt', encoding='utf8') as f:
    content = f.read()
    __author__, __email__, __license__, __version__ = filter(None, (
        re.search(rf"__{name}__ = '([^']+)'", content).group(1)
        for name in ('author', 'email', 'license', 'version')
        ))


setup(
    name='uactor',
    version=__version__,
    url=repository,
    license=__license__,
    author=__author__,
    author_email=__email__,
    description='uActor multiprocessing microframework',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        ],
    keywords=['actor', 'multiprocessing'],
    py_modules=['uactor'],
    test_suite='tests',
    platforms=['posix', 'win32', 'darwin'],
    zip_safe=True,
    )

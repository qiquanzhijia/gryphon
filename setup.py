#!/usr/bin/env python
from __future__ import print_function
import os
import re
import sys
from operator import lt, gt, eq, le, ge
from os.path import (
    abspath,
    dirname,
    join,
)
from distutils.version import StrictVersion
from setuptools import (
    Extension,
    find_packages,
    setup,
    Command,
)
import versioneer

class LazyBuildExtCommandClass(dict):
    """
    Lazy command class that defers operations requiring Cython and numpy until
    they've actually been downloaded and installed by setup_requires.
    """

    def __contains__(self, key):
        return (
            key == 'build_ext'
            or super(LazyBuildExtCommandClass, self).__contains__(key)
        )

    def __setitem__(self, key, value):
        if key == 'build_ext':
            raise AssertionError("build_ext overridden!")
        super(LazyBuildExtCommandClass, self).__setitem__(key, value)

    def __getitem__(self, key):
        if key != 'build_ext':
            return super(LazyBuildExtCommandClass, self).__getitem__(key)

        from Cython.Distutils import build_ext as cython_build_ext
        import numpy

        # Cython_build_ext isn't a new-style class in Py2.
        class build_ext(cython_build_ext, object):
            """
            Custom build_ext command that lazily adds numpy's include_dir to
            extensions.
            """

            def build_extensions(self):
                """
                Lazily append numpy's include directory to Extension includes.

                This is done here rather than at module scope because setup.py
                may be run before numpy has been installed, in which case
                importing numpy and calling `numpy.get_include()` will fail.
                """
                numpy_incl = numpy.get_include()
                for ext in self.extensions:
                    ext.include_dirs.append(numpy_incl)

                super(build_ext, self).build_extensions()

        return build_ext


# def window_specialization(typename):
#     """Make an extension for an AdjustedArrayWindow specialization."""
#     return Extension(
#         'catalyst.lib._{name}window'.format(name=typename),
#         ['catalyst/lib/_{name}window.pyx'.format(name=typename)],
#         depends=['catalyst/lib/_windowtemplate.pxi'],
#     )

class CleanCommand(Command):
    """
    Custom clean command to tidy up the project root, because even
        python setup.py clean --all
    doesn't remove build/dist and egg-info directories, which can and have caused
    install problems in the past.
    """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


with open('README.md', 'r') as f:
    long_description = f.read()

SYS_VERSION = '.'.join(list(map(str, sys.version_info[:3])))

setup(
    name='gryphon',
    packages=find_packages(),
    version=versioneer.get_version(),
    author='MacLeod & Robinson, Inc.',
    author_email='hello@tinkercorp.com',
    description='A framework for running algorithmic trading strategies on cryptocurrency markets.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://www.gryphonframework.org',
    classifiers=(
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'License :: Other/Proprietary License',
    ),
    entry_points={
        'console_scripts': [
            'gryphon-runtests=gryphon.tests.runtests:main',
            'gryphon-exec=gryphon.execution.app:main',
            'gryphon-cli=gryphon.execution.console:main',
            'gryphon-dashboards=gryphon.dashboards.app:main',
        ],
    },
    include_package_data=True,
    install_requires=[
        'alembic==0.6.0',
        'Babel==2.6.0',
        'backports.shutil-get-terminal-size==1.0.0',
        'cement==2.10.12',
        'certifi==2018.4.16',
        'chardet==3.0.4',
        'coinbase==1.0.4',
        'contextlib2==0.5.5',
        'Cython==0.20.1',
        'decorator==4.3.0',
        'Delorean>=1.0.0,<2',
        'enum34==1.1.6',
        'futures==3.2.0',
        # 'decimal==2.3',
        'idna==2.7',
        'ipython==5.7.0',
        'ipython-genutils==0.2.0',
        'line-profiler==2.1.2',
        'Mako==1.0.7',
        'MarkupSafe==1.0',
        'mock==3.0.5',
        'more-itertools>=4.2.0,<5',
        # 'MySQL-python==1.2.5',
        'nose==1.3.7',
        'pathlib2==2.3.2',
        'pexpect==4.6.0',
        'pickleshare==0.7.4',
        'prompt-toolkit==1.0.15',
        'ptyprocess==0.6.0',
        'Pygments==2.2.0',
        # 'pylibmc>=1.5.2,<2',
        'python-dotenv==0.10.3',
        'pytz==2018.5',
        'raven==6.9.0',
        'rednose>=1.3.0,<2',
        'redis==2.10.6',
        'requests==2.22.0',
        'requests-futures==0.9.7',
        'requests-toolbelt==0.8.0',
        'retrying==1.3.3',
        'scandir==1.7',
        'simplegeneric==0.8.1',
        'six==1.12.0',
        'sure==1.4.11',
        'SQLAlchemy>=1.2.18',
        'termcolor==1.1.0',
        'traitlets==4.3.2',
        'tzlocal==2.0.0',
        'urllib3==1.23',
        'wcwidth==0.1.7',
        'websocket-client==0.48.0',
    ],
    cmdclass=LazyBuildExtCommandClass(versioneer.get_cmdclass()),
    # cmdclass={
    #     'clean': CleanCommand,
    #     'build_ext': build_ext,
    # },
)

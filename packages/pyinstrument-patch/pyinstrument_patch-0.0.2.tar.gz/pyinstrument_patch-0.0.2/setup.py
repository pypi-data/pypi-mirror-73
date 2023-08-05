from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyinstrument_patch',
    packages=['pyinstrument_patch'],
    version='0.0.2',
    license='MIT',
    description='Patch for fix pyinstrument root_frame exception',
    author='PhuongTMR',
    author_email='phuong@paradox.ai',
    url='https://github.com/PhuongTMR/pyinstrument_patch.git',
    download_url='https://github.com/PhuongTMR/pyinstrument_patch/archive/master.zip',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='Pyinstrument Patch',
    install_requires=[
        'pyinstrument>=3.1.3'
    ]
)

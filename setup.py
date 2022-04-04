'''
Author: Yingjie Peng
Date: 2022-04-04 13:14:56
LastEditTime: 2022-04-04 17:41:01
LastEditors: Yingjie Peng
Description: Define by yourself
FilePath: /QC/setup.py

'''
# create setup.py
import sys
sys.path.append("./")
from setuptools import setup, find_packages
from qualc import __version__
def load_requires(file_name="./requirements.txt"):
    with open(file_name) as f:
        requires = f.read().split('\n')[:-1]
    return requires

setup(
    name='qualc',
    version=__version__,
    packages= ['qualc', 'qualc.func', 'qualc.mri', 'qualc.freesurfer'],
    url='',
    license='',
    author='Yingjie Peng',
    author_email='hlpureboy@gmail.com',
    description='',
    python_requires='>=3.6',
    # command_line
    entry_points={
        'console_scripts': [
            'qualc = qualc.command:main',
        ],
    },
    install_requires=load_requires(),
    package_data={
        'qualc':['template/*'],
    }

)
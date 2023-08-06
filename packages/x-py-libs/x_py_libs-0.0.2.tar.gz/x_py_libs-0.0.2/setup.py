# -*- coding=utf-8 -*-

from distutils.core import setup

from setuptools import setup, find_packages

setup(
    name="x_py_libs",
    version="0.0.2",
    # keywords = ("pip", "license","licensetool", "tool", "gm"),
    # description = "设备指纹获取、license生成、指纹与有效期验证工具",
    # long_description = "设备指纹获取、license生成、指纹与有效期验证工具",
    license="MIT Licence",

    # url = "https://github.com/gm19900510/licensetool",
    author="xiaxiazhu",
    author_email="xiaxiazhu147@gmail.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        'psycopg2', 'pyodbc',
        'tornado',
        'Flask', 'Flask_Cors', 'Flask_RESTful',
        'redis',
        'six', 'pymediainfo', 'itsdangerous','Werkzeug',
        'requests',
        'pycrypto'
    ]
)


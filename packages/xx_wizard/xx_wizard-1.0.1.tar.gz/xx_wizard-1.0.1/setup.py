# -*- coding: utf-8 -*-
"""
 **********************************************************
 * Author        : tianshl
 * Email         : email@example.com
 * Last modified : 2020-07-09 09:46:52
 * Filename      : setup.py
 * Description   : 
 * ********************************************************
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='xx_wizard',                           # 名称
    version='1.0.1',                            # 版本号
    description='xx精灵',                        # 简单描述
    long_description=long_description,          # 详细描述
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords='keyboard mouse pynput tkinter wizard',  # 关键字
    author='tianshl',                                 # 作者
    author_email='xiyuan91@126.com',                  # 邮箱
    url='https://my.oschina.net/tianshl/blog',        # 包含包的项目地址
    license='MIT',                                    # 授权方式
    packages=find_packages(),                         # 包列表
    install_requires=['pynput'],
    include_package_data=True,
    zip_safe=True,
)

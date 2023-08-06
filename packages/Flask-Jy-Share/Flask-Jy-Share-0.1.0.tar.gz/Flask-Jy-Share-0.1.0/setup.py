'''
Flask-Jy-Share
~~~~~~~~~~~~~~~
Create social share component in Jinja2 template based on share.js.
:copyright: (c) 2020 by jiangyang.
:license: MIT, see LICENSE for more details.
'''
from os import path
from codecs import open
from setuptools import setup

basedir = path.abspath(path.dirname(__file__))


# 从 README 中读取描述
with open(path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Flask-Jy-Share',
    version='0.1.0',
    url='https://github.com/jiangyanglinlan/flask-share',
    license='MIT',
    author='jiangyang',
    author_email='jiangyanglinlan@qq.com',
    description='Create social share component in Jinja2 template based on share.js.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # 长描述内容模型
    platforms='any',
    packages=['flask_share'],  # 包含的包列表
    zip_safe=False,
    test_suite='test_flask_share',
    include_package_data=True,
    install_requires=[
        'Flask',
    ],
    keywords='flask extension development',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

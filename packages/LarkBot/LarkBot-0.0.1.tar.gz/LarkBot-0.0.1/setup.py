'''
@Author: your name
@Date: 2020-07-04 22:29:41
@LastEditTime: 2020-07-05 01:19:42
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /feishuBot/setup.py
'''

import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="LarkBot",
  version="0.0.1",
  author="Xie Hengjian",
  author_email="xiehengjian@outlook.com",
  description="A sdk of Lark",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/xiehengjian/LarkBot",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
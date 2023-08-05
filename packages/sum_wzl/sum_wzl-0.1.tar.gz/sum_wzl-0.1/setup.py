import setuptools
from setuptools import setup , find_packages
setup(
    # name = "wzl_sum",
    name = "sum_wzl",
    version = "0.1",
    description = "find the sum from begin number to end number, end number included",
    # url="https://github.com/wangzl/wzl_sum",
    # long_description = LONG_DESCRIPTION,
    author = "wangzhaoliang",
    author_email = "sa516326@mail.ustc.edu.cn",
    license = "Apache",
    # packages = ["wzl_sum"],
    packages = find_packages(),
)

import os

from setuptools import setup, find_packages


def gen_data_files(*dirs):
    """打包不规则格式数据"""
    results = []

    for src_dir in dirs:
        for root,dirs,files in os.walk(src_dir):
            results.append((root, map(lambda f:root + "/" + f, files)))
    return results


setup(
    name="startS",
    version="0.1.2",
    description="生成启动,停止,重启以及自检启动脚本",
    long_description="快速生成启动,停止,重启以及自检启动脚本",
    # url="https://github.com/pansj66/serverD",
    author="shijiang Pan",
    author_email="1377161366@qq.com",
    license="MIT Licence",
    packages=find_packages(include=[
        "startS", "startS.*",

    ]),
    #
    # packages=find_packages(include=[
    #     "serverD", "serverD.*",
    #     "serverE", "serverE.*",
    # ]),
    include_package_data=True,

    data_files=gen_data_files("startS/base_sh"),
    platforms=["all"],

    entry_points={
        'console_scripts': [
            "startS = startS.produce:run",
        ]
    },

)

# print(gen_data_files("serverD/serverE"))

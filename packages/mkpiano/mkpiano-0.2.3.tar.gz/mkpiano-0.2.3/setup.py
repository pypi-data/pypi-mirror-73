# -*- coding: utf-8 -*
import os
from setuptools import setup
from glob import glob

dirs = ['mkpiano']
modules = ['mkpiano']
for path,dir_list,file_list in os.walk("./mkpiano"):
    for dir_name in dir_list:
        if dir_name.find("__")==-1 and dir_name.find("egg")==-1:
            dirs.append((path+"/"+dir_name).replace("/",".").replace("..",""))
    for file_name in file_list:
        if file_name.find(".py")!=-1 and file_name.find(".pyc")==-1:
            modules.append((path+"."+file_name.replace(".py","")).replace("/",".").replace("..",""))

here = os.path.dirname(__file__)
setup(
    name='mkpiano',
    version='0.2.3',
    author='makeblock',
    author_email='flashindream@gmail.com',
    url='https://makeblock.com',
    description=u'library for makeblock fingertip piano',
    packages=dirs,
    data_files=[
        (here+'/mkpiano/driver',glob('./assets/*.*')),
        (here+'/mkpiano/driver/DRVSETUP64',glob('./assets/DRVSETUP64/*.*'))
    ],
    py_modules=modules,
    install_requires=['pyserial'],
    include_package_data=True,
)
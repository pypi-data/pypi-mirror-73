import importlib
try:
    importlib.import_module('numpy')
except ImportError:
    from pip._internal import main as _main
    _main(['install', 'numpy'])

from setuptools import setup, Extension, find_packages
import setuptools
import numpy
import sys
import os
from distutils.sysconfig import get_python_lib
import shutil

# To use a consistent encoding
from codecs import open

from os import path
here = path.abspath(path.dirname(__file__))

# Looks for igeLibs in current project libs
igeLibsPath = 'igeLibs'

# Looks for global environment variable
if not path.exists(igeLibsPath):
    igeLibsPath = os.environ.get('IGE_LIBS')

# If not exist, then error
if not path.exists(igeLibsPath):
    print("ERROR: IGE_LIBS was not set!")
    exit(0)

firebase_sdk = path.join(igeLibsPath, 'firebase_cpp_sdk')
inc_dir = firebase_sdk + '/include'
lib_dir = firebase_sdk + '/libs/windows/VS2015/MD'
json_inc_dir = path.join(igeLibsPath, 'json/include/json')

is64Bit = sys.maxsize > 2 ** 32
if is64Bit:
    lib_dir = lib_dir + '/x64/Release'
else:
    lib_dir = lib_dir + '/x86/Release'

sfc_module = Extension('igeFirebase',
                    sources=[
                        'igeFirebase.cpp',
                        'igeFirebaseAnalytics.cpp',
                        'igeFirebaseAuth.cpp',
                        'igeFirebaseMessaging.cpp',
                        'igeFirebaseRemoteConfig.cpp',
                        'igeFirebaseMLKit.cpp',
                        'igeFirebaseFirestore.cpp',
                        'Firebase.cpp',
                        'FirebaseAnalytics.cpp',
                        'FirebaseAuth.cpp',
                        'FirebaseMessaging.cpp',
                        'FirebaseRemoteConfig.cpp',
                        'FirebaseMLKit.cpp',
                        'FirebaseFirestore.cpp',
                        'dispatch_queue.cpp',
                        'win32/FirebaseImpl.cpp',
                        'win32/FirebaseMLKitImpl.cpp',
                    ],
                    include_dirs=[inc_dir, json_inc_dir, './', './win32'],
                    library_dirs=[lib_dir],
                    libraries=['firebase_app',
                        'firebase_remote_config',
                        'firebase_analytics',
                        'firebase_auth',
                        'firebase_messaging',
                        'firebase_app',
                        'advapi32',
                        'ws2_32',
                        'crypt32',
                        'rpcrt4',
                        'ole32',
                        'kernel32',
                        'user32',
                        'gdi32',
                        'winspool',
                        'shell32',
                        'oleaut32',
                        'uuid',
                        'comdlg32'
                    ])

setup(name='igeFirebase', version='0.0.19',
        description= 'C++ extension Firebase for 3D and 2D games.',
        author=u'Indigames',
        author_email='dev@indigames.net',
        packages=find_packages(),
        ext_modules=[sfc_module],
        long_description=open(path.join(here, 'README.md')).read(),
        long_description_content_type='text/markdown',

        # The project's main homepage.
        url='https://indigames.net/',

        license='MIT',
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            #'Operating System :: MacOS :: MacOS X',
            #'Operating System :: POSIX :: Linux',
            'Operating System :: Microsoft :: Windows',
            'Topic :: Games/Entertainment',
        ],
        # What does your project relate to?
        keywords='Firebase 3D game Indigames',
      )

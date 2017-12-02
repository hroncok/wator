from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='wator',
    ext_modules=cythonize('wator/_cwator.pyx'),
    include_dirs=[numpy.get_include()],
    install_requires=[
        'Cython',
        'NumPy',
    ],
    license='Public Domain',
    classifiers=[
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    ]
)

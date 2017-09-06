from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='wator',
    ext_modules=cythonize('wator.pyx'),
    include_dirs=[numpy.get_include()],
    install_requires=[
        'Cython',
        'NumPy',
    ],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ]
)

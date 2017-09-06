from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='wator',
    name='maze',
    ext_modules=cythonize('wator/_cwator.pyx'),
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

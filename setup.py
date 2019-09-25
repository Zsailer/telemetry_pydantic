"""
Setup module for the jupyterlab-telemetry
"""
from setuptools import setup, find_packages

setup(
    name='telemetry_pydantic',
    version='0.0.2',
    description='Event validation, schema generation, and logging in pure Python',
    packages=find_packages(),
    author          = 'Zach Sailer',
    author_email    = 'zachsailer@gmail.com',
    url             = 'https://github.com/Zsailer/telemetry_pydantic',
    license         = 'BSD 3',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['pydantic', 'telemetry'],
    python_requires = '>=3.6',
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'jupyter_telemetry',
        'pydantic',
        'traitlets'
    ],
)

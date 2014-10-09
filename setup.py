from setuptools import find_packages
from setuptools import setup


VERSION = '0.0.1'


setup(
    author='Ricardo M. Vilchis',
    author_email="ajkaanba@gmail.com",
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
    description='A Python API for PayU Latam',
    entry_points={
        # "EntryPoint must be in 'name=module:attrs [extras]' format"
    },
    install_requires=[
        'requests',
    ],
    keywords='payu',
    license='MIT',
    long_description=(
        open('README.rst').read() + '\n' +
        open('CHANGES.rst').read()
    ),
    name='payup',
    packages=find_packages(),
    test_suite='payu.tests',
    tests_require=[
        'mock',
        'pytest',
    ],
    url='https://github.com/ajkaanbal/payu',
    version=VERSION,
    zip_safe=False,
)

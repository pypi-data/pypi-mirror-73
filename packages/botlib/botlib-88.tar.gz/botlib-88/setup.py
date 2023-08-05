# setup.py
#
#

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='botlib',
    version='88',
    url='https://bitbucket.org/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description=""" BOTLIB is a library you can use to program bots. """,
    long_description=read(),
    long_description_content_type="text/x-rst",
    license='Public Domain',
    zip_safe=False,
    packages=["bot"],
    namespace_packages=["bot"],
    scripts=["bin/bot"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

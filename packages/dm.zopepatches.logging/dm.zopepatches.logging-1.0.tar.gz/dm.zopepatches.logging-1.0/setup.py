from os.path import abspath, dirname, join
try:
  # try to use setuptools
  from setuptools import setup
  setupArgs = dict(
      include_package_data=True,
      namespace_packages=['dm', 'dm.zopepatches'],
      zip_safe=False,
      entry_points = dict(
        ),
      install_requires = ["zExceptions"],
      )
except ImportError:
  # use distutils
  from distutils import setup
  setupArgs = dict(
    )

cd = abspath(dirname(__file__))
pd = join(cd, 'dm', 'zopepatches', 'logging')

def pread(filename, base=pd): return open(join(base, filename)).read().rstrip()

setup(name='dm.zopepatches.logging',
      version=pread('VERSION.txt').split('\n')[0],
      description="Use Zope exception format for logging",
      long_description=pread('README.txt'),
      classifiers=[
#        'Development Status :: 3 - Alpha',
       'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Framework :: Zope',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        ],
      author='Dieter Maurer',
      author_email='dieter@handshake.de',
      url='https://pypi.org/project/dm.zopepatches.logging',
      packages=['dm', 'dm.zopepatches', 'dm.zopepatches.logging'],
      keywords='logging Zope exception',
      license='BSD',
      **setupArgs
      )

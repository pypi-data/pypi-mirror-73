from setuptools import setup

DISTNAME = 'DEWAKSS'
VERSION = '0.999999'
DESCRIPTION = "Denoising Expression data with a Weighted Affinity Kernel and Self-Supervision."
# with open('README.rst') as f:
#     LONG_DESCRIPTION = f.read()
MAINTAINER = 'Andreas Tjarnberg'
MAINTAINER_EMAIL = 'andreas.tjarnberg@nyu.edu'
URL = 'https://gitlab.com/Xparx/dewakss'
DOWNLOAD_URL = 'https://gitlab.com/Xparx/dewakss/-/archive/Tjarnberg2020branch/dewakss-Tjarnberg2020branch.zip'
LICENSE = 'LGPL'


setup(name=DISTNAME,
      version=VERSION,
      description=DESCRIPTION,
      url=URL,
      author=MAINTAINER,
      author_email=MAINTAINER_EMAIL,
      license=LICENSE,
      packages=['dewakss'],
      python_requires='>=3.6',
      install_requires=[
          'sparse-dot-mkl',
          'umap-learn==0.3.10',
          'scipy',
          'sklearn',
          'pandas',
          'scanpy>=1.5.1',
          'scvelo',
          'matplotlib',
          'seaborn',
      ],
      zip_safe=False)

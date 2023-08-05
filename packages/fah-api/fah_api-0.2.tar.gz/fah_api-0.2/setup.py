from distutils.core import setup

#with open('README.md', 'r') as fh:
#  long_description = fh.read()

setup(
  name = 'fah_api',
  packages = ['fah_api'],
  version = '0.2',
  license='MIT',
  description = 'A python3 library for controlling Folding@Home clients',
#  long_description = long_description,
#  long_description_content_type='text/markdown',
  author = 'Ben Cordes',
  author_email = 'cordes.ben@gmail.com',
  url = 'https://github.com/fraterrisus/fah-api-python',
  download_url = 'https://github.com/fraterrisus/fah-api-python/archive/v0.2.tar.gz',
  keywords = ['foldingathome'],
  install_requires=[],
  python_requires='>=3',
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: End Users/Desktop',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Topic :: Software Development :: Libraries',
    'Topic :: Home Automation',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
)

from setuptools import setup, find_packages

setup(
  name = 'classier',
  packages = find_packages(),
  version = '0.0.8',
  license='MIT',
  description = 'Make your classes classier.',
  author = 'Ozgen Eren',
  author_email = 'ozgeneral@gmail.com',
  url = 'https://github.com/ozgeneral/classier',
  download_url = 'https://github.com/ozgeneral/classier/archive/0.0.8.tar.gz',
  keywords = ['classier', 'utils', 'convenience'],
  install_requires=[
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
  ],
)

from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: BSD License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Solidity',
  version='0.0.3',
  description='Python interface for the Solidity FDEM code',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Dr Ado Farsi',
  author_email='adofarsi@gmail.com',
  license='BSD', 
  classifiers=classifiers,
  keywords='', 
  packages=find_packages(),
  install_requires=[''] 
)
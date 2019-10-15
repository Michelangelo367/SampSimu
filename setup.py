from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='SampSimu',
      version='0.1',
      description=' ',
      long_description=readme(),
      url='  ',
      author='Siavash Tabrizian',
      author_email='stabrizian@gmail.com',
      license='MIT',
      packages=['SampSimu'],
      install_requires=[ 'numpy','scipy' ],
      zip_safe=False)
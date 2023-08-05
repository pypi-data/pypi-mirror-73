from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='mkctools',
      version='0.3',
      description='Machine Learning Libraries',
      url='http://github.com/mc6666/mkctools',
      author='Michael Chen',
      author_email='mc6666@gmail.com',
      license='MIT',
      packages=['mkctools'],
      zip_safe=False)
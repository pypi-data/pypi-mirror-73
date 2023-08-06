from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(name='pydublinbus',
      version='0.0.2',
      description='Python library to get the real-time transport information (RTPI) for Dublin Bus',
      long_description=long_description,
      long_description_content_type="text/markdown",
      keywords='dublin bus RTPI',
      author='Alex Iepuras',
      author_email='iepuras.alex@gmail.com',
      license='MIT',
      url='https://pypi.org/project/pydublinbus/0.0.1/',
      download_url='https://pypi.org/project/pydublinbus/0.0.1/#files',
      platforms=["any"],
      packages=find_packages(),
      zip_safe=False,
      python_requires='>=3.6',
      install_requires=[
          'requests',
      ],
      tests_requires=[
          'tox',
          'flake8',
          'pylint',
          'pytest'
      ]
     )

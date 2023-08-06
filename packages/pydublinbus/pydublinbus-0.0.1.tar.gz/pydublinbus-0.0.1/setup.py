from setuptools import setup, find_packages

setup(name='pydublinbus',
      version='0.0.1',
      description='Python library to get the real-time transport information (RTPI) from Dublin Bus',
      keywords='dublin bus RTPI',
      author='Alex Iepuras',
      author_email='iepuras.alex@gmail.com',
      license='MIT',
      url='',
      download_url='',
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

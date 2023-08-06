import setuptools
from setuptools import setup

setup(name='ondine_laser_control',
      version='0.1.0',
      description='Control laser attachment on OpenTrons robot',
      author='Caden Keese',
      author_email='ckeese@ondinebio.com',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'opentrons==*',
          'pyserial==*',
          'pydantic==*'
      ],
      include_package_data=True,
      zip_safe=False)

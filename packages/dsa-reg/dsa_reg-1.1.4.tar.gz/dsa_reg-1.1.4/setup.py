from __future__ import absolute_import, division, print_function
import os
import setuptools 

base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

setuptools.setup(
      name='dsa_reg',
      version='1.1.4',
      description='Register DSA items thumbnails and return homography matrix, image size,  x offset, y offset, scale x, and scale y. The registration code is based on OpenCV',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/mmasoud1/dsa_reg.git',
      author='Mohamed Masoud',
      author_email='mmasoud2@outlook.com',
      packages=setuptools.find_packages(),      
      license='MIT',
      install_requires=[
          'girder-client',
          'six', 
          'Pillow',
          'opencv-python',
      	  'scikit-image', 
      ],
      zip_safe=False,
      python_requires='>=2.7',      
      )

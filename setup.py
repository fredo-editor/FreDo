# Parts of this file were derived from the setup.py file of scikit-image
# scikit-image license can be found at
# https://github.com/scikit-image/scikit-image/blob/master/LICENSE.txt

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]

setup(name='FreDo-Editor',
      version='0.1.0_dev',
      description='Frequency Domain Image Editor',
      author='Vighnesh Birodkar',
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES,
      author_email='vighneshbirodkar@nyu.edu',
      entry_points={
          'gui_scripts': ['fredo = fredo.editor.main:run']
      }
      )

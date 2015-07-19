from setuptools import setup, find_packages

setup(name='FreDo Editor',
      version='0.1',
      description='Frequency Domain Image Editor',
      author='Vighnesh Birodkar',
      packages=find_packages(),
      author_email='vighneshbirodkar@nyu.edu',
      entry_points={
      'gui_scripts': [
          'fredo = fredo.editor.main:run',
      ]
      }
      )

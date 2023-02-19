import os
import pathlib

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext as build_ext_orig

def Test2(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        print(path)
        if os.path.isdir(path):
            Test2(path)

# Based off of https://stackoverflow.com/a/48015772/6505507

class CMakeExtension(Extension):
  def __init__(self, name):
    super().__init__(name, sources=[])

class build_ext(build_ext_orig):
  def run(self):
    for ext in self.extensions:
      self.build_cmake(ext)
    super().run()

  def build_cmake(self, ext):
    cwd = os.path.join(pathlib.Path().absolute(), ext.name)
    print(ext.name)

    # these dirs will be created in build_py, so if you don't have
    # any python sources to bundle, the dirs will be missing
    build_temp = pathlib.Path(self.build_temp)
    build_temp.mkdir(parents=True, exist_ok=True)
    extdir = pathlib.Path(self.get_ext_fullpath(ext.name))
    extdir.mkdir(parents=True, exist_ok=True)
    lib_out_path = os.path.join(extdir.parent.absolute(), "extract-xiso")

    # example of cmake args
    config = 'Debug' if self.debug else 'Release'
    cmake_args = [
        '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + str(lib_out_path),
        '-DCMAKE_BUILD_TYPE=' + config
    ]

    # example of build args
    build_args = [
        '--config', config,
        '--', '-j4'
    ]

    os.chdir(str(build_temp))
    self.spawn(['cmake', str(cwd)] + cmake_args)
    if not self.dry_run:
        self.spawn(['cmake', '--build', '.'] + build_args)
    # Troubleshooting: if fail on line above then delete all possible 
    # temporary CMake files including "CMakeCache.txt" in top level dir.
    Test2(cwd)
    os.chdir(str(cwd))

setup(
    name='extract-xiso-python',
    version='0.1',
    description='Simple python wrapper for some functionality of extract-xiso',
    url='https://github.com/dj0wns/extract-xiso-python',
    author='dj0wns',
    author_email='derekjones@asu.edu',
    license="Unlicense",
    packages=['extract-xiso-python'],
    ext_modules=[CMakeExtension('extract-xiso-python/extract-xiso')],
    cmdclass={
        'build_ext': build_ext,
    }
)

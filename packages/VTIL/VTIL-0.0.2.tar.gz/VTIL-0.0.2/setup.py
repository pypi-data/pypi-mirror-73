#! /usr/bin/python3
from distutils.command.install_data import install_data
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install_lib import install_lib
import platform
import sys
import os
import shutil


VERSION = '0.0.2'
CORE_COMMIT = '8bf3480'
PYBIND11_COMMIT = 'd54d6d8'


class CMakeExtension(Extension):
    def __init__(self, name, src_dir, additional=None, sources=None):
        if not sources:
            sources = []
            for dir_path, _, files in os.walk(src_dir):
                for file_name in files:
                    sources.append(os.path.join(dir_path, file_name))
            if additional:
                sources.extend(additional)

        super().__init__(name=name, sources=sources)


class InstallCMakeLibs(install_lib):
    def run(self):
        self.skip_build = os.path.exists('build/vtil.pyd')
        self.distribution.data_files = [
            ('vtil', ['wrappers/__init__.py', 'build/vtil.pyd']),
            ('vtil/arch', ['wrappers/arch/__init__.py']),
            ('vtil/common', ['wrappers/common/__init__.py']),
            ('vtil/compiler', ['wrappers/compiler/__init__.py']),
            ('vtil/symex', ['wrappers/symex/__init__.py'])
        ]

        super().run()


class BuildCMakeExtension(build_ext):
    def run(self):
        for extension in self.extensions:
            if extension.name == 'VTIL':
                self.build()

    def build(self):
        import git

        # Remove old build
        if not os.path.exists('build/vtil.pyd'):
            os.makedirs('build/lib', exist_ok=True)

            # Update submodules
            self.announce('Updating submodules ..')
            if os.path.exists('.git'):
                # We are running from a cloned version
                git.Repo('.').submodule_update(init=True, recursive=False)
            else:
                # We are running from a pypi tar.gz version
                if not os.path.exists('external/core'):
                    git.Repo.clone_from('https://github.com/vtil-project/VTIL-Core.git', 'external/core').git.checkout(CORE_COMMIT)
                if not os.path.exists('external/pybind11'):
                    git.Repo.clone_from('https://github.com/pybind/pybind11.git', 'external/pybind11').git.checkout(PYBIND11_COMMIT)

            if platform.system() == 'Windows':
                self.announce('Preparing build for Windows ..', level=3)
                self.spawn(self.build_for_windows())
            elif platform.system() == 'Linux':
                pass
            elif platform.version() == 'Darwin':
                pass

            self.announce('Building ..', level=3)
            self.spawn(self.build_cmake())

        self.announce('Generating libs ..', level=3)
        self.spawn(self.gen_libs())

    @staticmethod
    def build_for_windows():
        import cmakegenerators

        if 'Visual Studio 16 2019' not in [gen.name for gen in cmakegenerators.get_generators()]:
            raise Exception('Visual Studio 2019 not found')

        return \
            [
                'cmake',
                '-DPYTHON_EXECUTABLE=' + sys.executable,
                '-G', 'Visual Studio 16 2019',
                '-S', '.',
                '-B', 'build'
            ]

    @staticmethod
    def build_cmake():
        return \
            [
                'cmake',
                '--build', 'build',
                '--config', 'Release'
            ]

    @staticmethod
    def gen_libs():
        return \
            [
                "cmake",
                "--install", "build",
                "--component", "pyd",
                "--prefix", "build"
            ]


setup(
    name='VTIL',
    version=VERSION,
    author='Daniel. (@L33T)',
    description='Virtual-machine Translation Intermediate Language',
    long_description='VTIL Project, standing for Virtual-machine Translation Intermediate Language, is a set of tools'
                     ' designed around an optimizing compiler to be used for binary de-obfuscation and'
                     ' de-virtualization.\n\nThe main difference between VTIL and other optimizing compilers such as '
                     'LLVM is that it has an extremely versatile IL that makes it trivial to lift from any'
                     ' architecture including stack machines. Since it is built for translation, VTIL does not abstract'
                     ' away the native ISA and keeps the concept of the stack, physical registers, and the non-SSA'
                     ' architecture of a general-purpose CPU as is. Native instructions can be emitted in the middle '
                     'of the IL stream and the physical registers can be addressed from VTIL instructions freely.\n\n'
                     'VTIL also makes it trivial to emit code back into the native format at any virtual address'
                     ' requested without being constrained to a specific file format.',
    url='https://github.com/vtil-project/VTIL-Python',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: C++',
        'Topic :: Education'
    ],
    python_requires='>=3.4',
    license='BSD 3-Clause "New" or "Revised" License',
    cmdclass={
        'build_ext': BuildCMakeExtension,
        'install_lib': InstallCMakeLibs
    },
    setup_requires=['cmake>=3.15', 'cmake-generators', 'GitPython', 'future_fstrings'],
    ext_modules=[CMakeExtension('VTIL', src_dir='src', additional=['LICENSE.md', 'CMakeLists.txt'])],
    keywords='VTIL, VTIL Project, vtil, Virtual-machine Translation Intermediate Language, '
             'Translation Intermediate Language, Intermediate Language',
    zip_safe=False
)

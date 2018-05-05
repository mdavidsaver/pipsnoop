import sys
import os
import platform

from setuptools import Command, Distribution
from setuptools.command.build_ext import build_ext as _build_ext

from distutils.sysconfig import customize_compiler
from distutils.dep_util import newer_group
from distutils.util import get_platform
from distutils import log

Distribution.x_dsos = None

__all__ = (
    'build_dso',
    'build_ext',
)

def massage_dir_list(bdir, dirs):
    """Process a list of directories for use with -I or -L
    For relative paths, also include paths relative to a build directory
    """
    dirs = dirs or []
    dirs.extend([os.path.join(bdir, D) for D in dirs if not os.path.isabs(D)])
    return dirs

class build_dso(Command):
    description = "Build Dynamic Shared Object (DSO).  non-python dynamic libraries (.so, .dylib, or .dll)"

    # same as distutils.command.build_dso.build_ext
    # with the python specific bits (eg. swig) removed
    sep_by = " (separated by '%s')" % os.pathsep
    user_options = [
        ('build-lib=', 'b',
         "directory for compiled extension modules"),
        ('build-temp=', 't',
         "directory for temporary files (build by-products)"),
        ('plat-name=', 'p',
         "platform name to cross-compile for, if supported "
         "(default: %s)" % get_platform()),
        ('inplace', 'i',
         "ignore build-lib and put libraries into the source " +
         "directory alongside your pure Python modules"),
        ('include-dirs=', 'I',
         "list of directories to search for header files" + sep_by),
        ('define=', 'D',
         "C preprocessor macros to define"),
        ('undef=', 'U',
         "C preprocessor macros to undefine"),
        ('libraries=', 'l',
         "external C libraries to link with"),
        ('library-dirs=', 'L',
         "directories to search for external C libraries" + sep_by),
        ('rpath=', 'R',
         "directories to search for shared C libraries at runtime"),
        ('link-objects=', 'O',
         "extra explicit link objects to include in the link"),
        ('debug', 'g',
         "compile/link with debugging information"),
        ('force', 'f',
         "forcibly build everything (ignore file timestamps)"),
        ('compiler=', 'c',
         "specify the compiler type"),
        ('user', None,
         "add user include, library and rpath"),
        ]

    boolean_options = ['inplace', 'debug', 'force', 'swig-cpp', 'user']

    def initialize_options (self):
        self.dsos = None

        self.build_lib = None
        self.plat_name = None
        self.build_temp = None
        self.inplace = None
        #self.package = None

        self.include_dirs = None
        self.define = None
        self.undef = None
        self.libraries = None
        self.library_dirs = None
        self.rpath = None
        self.link_objects = None
        self.debug = None
        self.force = None
        self.compiler = None
        self.user = None


    def finalize_options(self):
        from distutils import sysconfig

        self.set_undefined_options('build_ext',
                                   ('build_lib', 'build_lib'),
                                   ('build_temp', 'build_temp'),
                                   ('compiler', 'compiler'),
                                   ('debug', 'debug'),
                                   ('force', 'force'),
                                   ('plat_name', 'plat_name'),
                                   ('inplace', 'inplace'),
                                   )

        self.dsos = self.distribution.x_dsos

        self.ensure_string_list('libraries')
        self.ensure_string_list('link_objects')

        # PATH-like lists
        for dlist in ['include_dirs', 'library_dirs', 'rpath']:
            strs = getattr(self, dlist, None) or []
            if isinstance(strs, str):
                strs = strs.split(os.pathsep)
            setattr(self, dlist, strs)

        #TODO comma seperated lists .define .undef

        self.include_dirs = massage_dir_list(self.build_temp, self.include_dirs)
        self.library_dirs = massage_dir_list(self.build_lib , self.library_dirs)

        # the linker of Darwin errors if asked to search non-existant directories
        self.library_dirs = list(filter(os.path.isdir, self.library_dirs))

    def run(self):
        if self.dsos is None:
            log.debug("No DSOs to build")
            return

        # the Darwin linker errors if given non-existant directories :(
        [self.mkpath(D) for D in self.library_dirs]

        log.info("Building DSOs")
        from distutils.ccompiler import new_compiler

        self.compiler = new_compiler(compiler=self.compiler,
                                     verbose=self.verbose,
                                     dry_run=self.dry_run,
                                     force=self.force)
        customize_compiler(self.compiler)

        if self.include_dirs is not None:
            self.compiler.set_include_dirs(self.include_dirs)
        if self.define is not None:
            # 'define' option is a list of (name,value) tuples
            for (name, value) in self.define:
                self.compiler.define_macro(name, value)
        if self.undef is not None:
            for macro in self.undef:
                self.compiler.undefine_macro(macro)
        if self.libraries is not None:
            self.compiler.set_libraries(self.libraries)
        if self.library_dirs is not None:
            self.compiler.set_library_dirs(self.library_dirs)
        if self.rpath is not None:
            self.compiler.set_runtime_library_dirs(self.rpath)
        if self.link_objects is not None:
            self.compiler.set_link_objects(self.link_objects)

        # fixup for MAC to build dylib (MH_DYLIB) instead of bundle (MH_BUNDLE)
        if sys.platform == 'darwin':
            for i,val in enumerate(self.compiler.linker_so):
                if val=='-bundle':
                    self.compiler.linker_so[i] = '-dynamiclib'

        # TODO: ABI tag (SONAME or similar)

        for dso in self.dsos:
            self.build_dso(dso)

    def _name2file(self, dso):
        prefix, suffix = 'lib', '.so'
        if sys.platform == 'darwin':
            suffix = '.dylib'
        elif sys.platform == "win32":
            prefix, suffix = '', '.dll'

        parts = dso.name.split('.')
        parts[-1] = '%s%s%s'%(prefix, parts[-1], suffix)
        return os.path.join(*parts)

    def build_dso(self, dso):
        baselib = self._name2file(dso)
        outlib = os.path.join(self.build_lib, baselib)
        sources = list(dso.sources)

        depends = sources + dso.depends
        if not (self.force or newer_group(depends, outlib, 'newer')):
            log.debug("skipping '%s' DSO (up-to-date)", dso.name)
            return
        else:
            log.info("building '%s' DSO as %s", dso.name, outlib)

        macros = dso.define_macros[:]
        for undef in dso.undef_macros:
            macros.append((undef,))

        extra_args = dso.extra_compile_args or []

        include_dirs = massage_dir_list(self.build_temp, dso.include_dirs or [])

        objects = self.compiler.compile(sources,
                                         output_dir=self.build_temp,
                                         macros=macros,
                                         include_dirs=include_dirs,
                                         debug=self.debug,
                                         extra_postargs=extra_args,
                                         depends=dso.depends)

        library_dirs = massage_dir_list(self.build_lib, dso.library_dirs or [])

        # the Darwin linker errors if given non-existant directories :(
        [self.mkpath(D) for D in library_dirs]

        if dso.extra_objects:
            objects.extend(dso.extra_objects)

        extra_args = []
        if sys.platform == 'darwin':
            # we always want to produce relocatable (movable) binaries
            extra_args.extend(['-install_name', '@loader_path/%s'%os.path.basename(baselib)])

        extra_args.extend(dso.extra_link_args or [])

        language = dso.language or self.compiler.detect_language(sources)

        self.compiler.link_shared_object(
            objects, outlib,
            libraries=dso.libraries,
            library_dirs=library_dirs,
            runtime_library_dirs=dso.runtime_library_dirs,
            extra_postargs=extra_args,
            export_symbols=[], #self.get_export_symbols(dso),
            debug=self.debug,
            build_temp=self.build_temp,
            target_lang=language)

        if self.inplace:
            self.copy_file(outlib, baselib)

class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)

        self.include_dirs = massage_dir_list(self.build_temp, self.include_dirs or [])
        self.library_dirs = massage_dir_list(self.build_lib , self.library_dirs or [])

    def run(self):
        self.run_command('build_dso')
        # the Darwin linker errors if given non-existant directories :(
        [self.mkpath(D) for D in self.library_dirs]
        _build_ext.run(self)

    def build_extension(self, ext):
        ext.include_dirs = massage_dir_list(self.build_temp, ext.include_dirs or [])
        ext.library_dirs = massage_dir_list(self.build_lib , ext.library_dirs or [])

        ext.extra_link_args = ext.extra_link_args or []

        if platform.system() == 'Linux':
            ext.extra_link_args.extend(['-Wl,-rpath,$ORIGIN'])

        # the Darwin linker errors if given non-existant directories :(
        [self.mkpath(D) for D in ext.library_dirs]

        _build_ext.build_extension(self, ext)

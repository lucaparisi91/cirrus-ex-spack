# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.packages.nvtx.package import Nvtx as BuiltinNvtx

from spack.package import *


class Nvtx(BuiltinNvtx):
    """Python code annotation library.

    Cirrus-ex override of the builtin NVTX package.

    The build environment is forced to use the standard-library ``distutils``
    implementation.  This avoids importing the vendored ``setuptools._distutils``
    package, which lacks ``distutils.msvccompiler`` and breaks the old
    ``numpy.distutils`` import chain exposed through the Cray PE Python
    ``PYTHONPATH`` during the NVTX Python extension build.
    """
    
    def setup_build_environment(self, env):
        super().setup_build_environment(env)
        env.set("SETUPTOOLS_USE_DISTUTILS", "stdlib")

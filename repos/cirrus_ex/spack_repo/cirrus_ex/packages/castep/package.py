# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class Castep(CMakePackage):
    """CASTEP is a software package to calculate the properties of materials.
    It is based on quantum mechanics, in a form known as density functional
    theory, and can simulate a wide range of materials proprieties including
    energetics, structure at the atomic level, vibrational properties, and
    many experimental characterisation methods, such as infra-red and Raman
    spectra, NMR, and core-level spectra.
    """

    homepage = "https://www.castep.org/home"
    manual_download = True
    url = "file://{0}/castep-24.1.tar.gz".format(os.getcwd())

    maintainers("NMannall")

    version("26.11", sha256="cd38ec9e87fd92b91fe7910179acad6486ee57935832846959151ec406fb5fb6")
    version("24.1", sha256="97d77a4f3ce3f5c5b87e812f15a2c2cb23918acd7034c91a872b6d66ea0f7dbb")


    depends_on("cray-fftw")
    depends_on("python")
    depends_on("py-pip", type="build")
    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("libxc")

    depends_on("c", type="build")  
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
    depends_on("gmake", type="build")
    depends_on("python", type=("build","run"))
    
    patch("24.1.patch", when="@24.1")
    patch("libxc_mod.patch", when="@24.1")

    def url_for_version(self, version):
        return "file://{0}/castep-{1}.tar.gz".format(
            os.getcwd(), version
        )

    def cmake_args(self):
        args = [
            self.define("BUILD", "fast"),
            self.define("COMMS_ARCH", "mpi"),
            self.define("FFT", "fftw3"),
            self.define("WITH_LIBXC", True)
        ]
        return args

    def setup_build_environment(self, env):
        # Ensure pip is available for the install phase via python -m pip
        # py-pip installs into the python prefix, not its own
        python_prefix = self.spec["python"].prefix
        env.prepend_path("PATH", python_prefix.bin)


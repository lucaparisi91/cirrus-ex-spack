# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.packages.openblas.package import Openblas as BuiltinOpenblas

from spack.package import *


class Openblas(BuiltinOpenblas):
    """OpenBLAS: An optimized BLAS library.

    Cirrus-ex override for CCE builds.

    OpenBLAS's ``f_check`` can misidentify Cray ``ftn`` as PGI.  That makes the
    OpenBLAS makefile pass PGI-only Fortran flags such as ``-tp`` and
    ``-Kieee`` to CCE, which CCE rejects.  This override forces the makefile to
    use the CRAY compiler path for ``+fortran`` builds with CCE.
    """
    
    @property
    def make_defs(self):
        make_defs = list(super().make_defs)
        
        if self.spec.satisfies("%cce") and "+fortran" in self.spec:
            make_defs.append("F_COMPILER=CRAY")

        return make_defs

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""MPICH override package for cirrus-ex-mpich environment.

This package inherits from the builtin MPICH package and adds the json-c
dependency required for MPICH 5.0+ when using the OFI netmod.

Root cause: MPICH 5.0's configure runs `pkg-config --static --libs libfabric.pc`
which pulls in Libs.private containing `-ljson-c`. The Cray libfabric.pc at
/opt/cray/libfabric/2.3.1/lib64/pkgconfig/libfabric.pc declares:
    Libs.private: -lcxi -lcurl -ljson-c -lm -latomic -lpthread -ldl

The system has libjson-c.so.5 (runtime) but no libjson-c.so development symlink,
causing the link to fail. Adding json-c as a spack dependency provides the
correct -I/-L/-rpath flags.
"""

from spack.package import *
from spack_repo.builtin.packages.mpich.package import Mpich as BuiltinMpich


class Mpich(BuiltinMpich):
    """MPICH with json-c dependency fix for version 5.0+."""

    # This is a derived package - inherit most metadata from builtin
    # Only override what's necessary to fix the build

    # Add json-c dependency for MPICH 5.0+ (required by libfabric's Libs.private)
    depends_on("json-c@0.18:", when="@5.0: netmod=ofi")

    def configure_args(self):
        """Add json-c configure argument for MPICH 5.0+."""
        args = super().configure_args()

        # For MPICH 5.0+ with OFI netmod, explicitly provide json-c path
        # This ensures the bundled json-c module uses the spack-built json-c
        if self.spec.satisfies("@5.0: netmod=ofi"):
            if "json-c" in self.spec:
                args.append("--with-json-c={0}".format(self.spec["json-c"].prefix))

        return args

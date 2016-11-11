import os
import subprocess

cwd = os.getcwd()

GAFFER_VERSION = "0.29.0.0"
ARNOLD_VERSION = "4.2.14.4"

ARNOLD_ROOT = "/Users/guide/Dev/eco/renderer/arnold/%s" % ARNOLD_VERSION
BUILD_DIR = "%s/dependencies/%s/osx" % (cwd, GAFFER_VERSION)
INSTALL_DIR = "%s/dist" % cwd
CXXFLAGS = ["-Wno-unused-local-typedefs",
            "-Wno-unused-parameter",
            # "-Wno-unused-but-set-variable",
            "-Wno-unused-variable",
            "-Wno-ignored-qualifiers"]
NO_GRAPHICS = True
NO_DOCS = True

gcc_atomic = "%s/include/boost/atomic/detail/gcc-atomic.hpp" % BUILD_DIR
patch = "%s/gcc-atomic.patch" % cwd
patch_cmd = "patch -p1 < %s" % patch

os.chdir(os.path.dirname(gcc_atomic))
p = subprocess.Popen(patch_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
out, _ = p.communicate()
if p.returncode == 0:
   print("=== Patching gcc-atomic.hpp ===")
   print(out)
os.chdir(cwd)

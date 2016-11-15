import os
import sys
import subprocess

cwd = os.getcwd()

arnold_dir = ""
arnold_dir_changed = False
deps_dir = ""
deps_dir_changed = False

try:
   with open("custom.cache", "r") as f:
      for l in f.readlines():
         spl = map(lambda x: x.strip(), l.split("="))
         if len(spl) == 2:
            if spl[0] == "DEPS_DIR" and os.path.isdir(spl[1]):
               deps_dir = spl[1]
            elif spl[0] == "ARNOLD_DIR" and os.path.isdir(spl[1]):
               arnold_dir = spl[1]
except:
   pass

for arg in sys.argv[1:]:
   if arg.startswith("DEPS_DIR="):
      tmp = arg[9:]
      if os.path.isdir(tmp):
         deps_dir = tmp
         deps_dir_changed = True
   elif arg.startswith("ARNOLD_DIR="):
      tmp = arg[11:]
      if os.path.isdir(tmp):
         arnold_dir = tmp
         arnold_dir_changed = True

if deps_dir_changed or arnold_dir_changed:
   with open("custom.cache", "w") as f:
      f.write("DEPS_DIR=%s\n" % deps_dir)
      f.write("ARNOLD_DIR=%s\n" % arnold_dir)
      f.write("\n")

print("Using ARNOLD_ROOT=%s" % arnold_dir)
print("Using BUILD_DIR=%s" % deps_dir)

ARNOLD_ROOT = arnold_dir
BUILD_DIR = deps_dir
INSTALL_DIR = "%s/dist" % cwd
CXXFLAGS = ["-Wno-unused-local-typedefs",
            "-Wno-unused-parameter",
            # "-Wno-unused-but-set-variable",
            "-Wno-unused-variable",
            "-Wno-ignored-qualifiers"]
NO_GRAPHICS = False
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

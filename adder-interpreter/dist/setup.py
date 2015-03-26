from distutils.core import setup
import distutils.sysconfig
prefix = distutils.sysconfig.EXEC_PREFIX
#print distutils.sysconfig.get_python_lib( True, False )
#print distutils.sysconfig.EXEC_PREFIX
setup(name = "adder", version = "0.3.3", author="Oliver Lavery", author_email="olavery@pivx.com",
      packages = ["adder", "adder.mosdef"],
      data_files = [
              ("", ["adderload.exe"]),
              ("DLLs", ["_adder.dll"]),
              ("adder-scripts",[
                  "adder-scripts/hello.py",
                  "adder-scripts/memtrace.py",
                  "adder-scripts/com_mon.py",
                  "adder-scripts/iesafe.py",
                  "adder-scripts/test.py"]),
              ("adder-scripts/graph",[
                  "adder-scripts/graph/graphtrace.py",
                  "adder-scripts/graph/trace2dot.py"])
          ]
      )



import importlib.util
import sys

if(len(sys.argv) > 1):
    print(sys.argv)
# directory = sys.argv[0]
spec = importlib.util.spec_from_file_location("epidemic-1.2.py", sys.argv[1])
print("hello \n")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)

foo.setup(foo.epidemic_model)
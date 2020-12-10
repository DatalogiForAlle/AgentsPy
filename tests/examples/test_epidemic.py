
import importlib.util
import sys
import os

# if(len(sys.argv) > 1):
#     print(sys.argv)
# directory = "tutorials/models/"
# directory = sys.argv[1]
directory = "./tutorials/models/"
directory_list = os.listdir(directory)
for  d in directory_list:
    if not d.endswith('.py'):
        continue
    print("Testing " + d)
    spec = importlib.util.spec_from_file_location(d, "tutorials/models/" + d)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "model_setup"):
        setupRan = True
        try:
            module.model_setup(module.epidemic_model)
        except:
            setupRan = False
        if setupRan:
            print("testing model_setup in "+ d +" succeeded")
        else:
            print("testing model_setup in  "+ d +" failed")
    
    if hasattr(module, "model_step"):
        step_ran = True
        for x in range(100):
            try:
                module.model_step(module.epidemic_model)
            except:
                step_ran = False
        if step_ran:
            print("testing model_step in "+ d +" succeeded")
        else:
            print("testing model_step in  "+ d +" failed")  
    print("")


# # Testing epidemic-1.2.py
# print("Testing epidemic-1.2.py")
# spec = importlib.util.spec_from_file_location("epidemic-1.2.py", "tutorials/models/epidemic-1.2.py")
# module = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(module)
# # print("running setup")
# setupRan = True
# try:
#     module.model_setup(module.epidemic_model)
# except:
#     setupRan = False
# if setupRan:
#     print("running Setup in epidemic-1.2.py succeeded")
# else:
#     print("running Setup in epidemic-1.2.py failed")
# # print("finish running setup")

    # foo.model_setup(foo.epidemic_model)
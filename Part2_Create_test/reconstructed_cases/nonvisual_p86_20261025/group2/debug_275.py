import importlib.util
from pathlib import Path
import numpy as np
from unittest.mock import patch
root=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('target_test',root/'issue_275/test.py')
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
original=np.linalg.eig
inputs=[]
def observe(matrix,*args,**kwargs):
    inputs.append(np.array(matrix,copy=True))
    return original(matrix,*args,**kwargs)
with patch.object(np.linalg,'eig',observe): ns,_=module.load_target()
print('inputs',[(a.shape,a.tolist()) for a in inputs])
for name,value in ns.items():
    if callable(getattr(value,'to_matrix',None)):
        matrix=value.to_matrix()
        print(name,type(value),type(matrix),matrix.shape,np.asarray(matrix).shape)
        print(matrix)

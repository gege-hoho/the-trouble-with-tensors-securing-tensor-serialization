import struct
import torch
import json
from safetensors.torch import save_file

tensors = {
    "embedding": torch.rand((2,2), dtype=torch.float32),
    "attention": torch.rand((2,3), dtype=torch.float32),
}
save_file(tensors, "model.safetensors")

output = {}
with open("model.safetensors", "rb") as f:
    header_length_bytes = f.read(8)
    header_length = struct.unpack("<Q", header_length_bytes)[0]
    start_of_data= 8 + header_length
    header_string = f.read(header_length).decode('utf-8')
    header = json.loads(header_string)

    for name, tensor_information in header.items():
        if tensor_information["dtype"] != "F32":
            raise ValueError("Tensor {} not supported".format(name))
        shape = tensor_information["shape"]
        start, end = tensor_information["data_offsets"]
        end += start_of_data
        start += start_of_data
        f.seek(start)
        data =[]
        while f.tell() < end:
            f32_bytes = f.read(4)
            f32 = struct.unpack("f", f32_bytes)[0]
            data.append(f32)
        output[name] = torch.tensor(data).reshape(tensor_information["shape"])


    for name, tensor in tensors.items():
        assert torch.equal(output[name], tensor)
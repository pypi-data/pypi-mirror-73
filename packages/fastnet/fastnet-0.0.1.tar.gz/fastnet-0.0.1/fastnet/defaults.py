import os
import numpy
import re

npType = numpy.float32

#PYTORCH_DEVICE can be: cpu, gpu, gpu:0, gpu:1, etc...
filt = re.compile('([a-z]+):?(\d?)')
grp = filt.match(os.environ.get('PYTORCH_DEVICE', 'cpu'))
device = grp.group(1)
id =  int(grp.group(2)) if grp.group(2) != '' else 0

def set_torch_defaults(torch):
    if device == 'gpu':
        torch.cuda.set_device(id)
        torch.set_default_tensor_type(torch.cuda.FloatTensor)
    else:
        torch.set_default_tensor_type(torch.FloatTensor)

    torch.set_default_dtype(torch.float32)

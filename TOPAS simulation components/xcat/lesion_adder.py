# This python helper file adds a mode 2 lesion binary XCAT file to a mode 0 whole body binary XCAT file.
# It works by replacing the activity value in any voxel in the mode 0 binary file with the activity in the corresponding voxel in the mode 2 binary file if the mode 2 voxel's activity is non-zero.

import struct

# reads in the mode 0 XCAT phantom (full body)
full_body_bin = open(r"", 'rb')
# reads in the heart lesion/spherical lesion/heart plaque
extra_phantom_bin = open(r"", 'rb')

# creates new phantom binary file
new_phantom_bin = open(r"", 'wb')

# determines number of bytes in the XCAT file
full_body_bin.seek(0,2)
num_bytes = full_body_bin.tell()
full_body_bin.seek(0)

i = 0
while i < num_bytes:
    # reads in 4 bytes = 32 bits
    full_body_chunk = full_body_bin.read(4)
    extra_chunk = extra_phantom_bin.read(4)
    
    # <f denotes little endian float encoding
    full_body_activity = struct.unpack("<f", full_body_chunk)[0]
    extra_chunk_activity = struct.unpack("<f", extra_chunk)[0]

    if extra_chunk_activity != 0:
        new_phantom_bin.write(extra_chunk)
    else:
        new_phantom_bin.write(full_body_chunk)

    # increments counter to next chunk
    i += 4 

full_body_bin.close()
extra_phantom_bin.close()
new_phantom_bin.close()
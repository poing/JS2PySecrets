#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#

from PIL import Image
import numpy as np
import random
import secrets



# Define image size
width = 200
height = 200

# Create a random dither bitmap image
#bitmap = np.random.randint(0, 256, (height, width), dtype=np.uint8)
#img = Image.fromarray(bitmap)

# rng = lambda bits: (bin(123456789)[2:].zfill(32) * -(-bits // 32))[-bits:]
# rng = lambda bits: bin(random.getrandbits(bits))[2:].zfill(bits)
rng = lambda bits: bin(secrets.randbits(bits))[2:].zfill(bits)
#print(rng(256*8))


row = []
col = []

chunk_size=8

long_string = rng(width*height*8)
print(len(long_string))
chunks = [int(long_string[i:i+chunk_size],2) for i in range(0, len(long_string), chunk_size)]
for m in range(height):
	for n in range(width):
		row.insert(n, chunks.pop(0))
	col.insert(m, row)
	row = []
    
#bitmap = [[random.randint(0, 255) for _ in range(width)] for _ in range(height)]
#bitmap = [[int(rng(8),2) for _ in range(width)] for _ in range(height)]

print(col[3])
img = Image.new('L', (width, height))


for y in range(height):
    for x in range(width):
        img.putpixel((x, y), col[y][x])
        
# Save the image
#print(bitmap)
#print(len(bitmap))
#print(len(bitmap[0]))
img.save("random_dither_bitmap.png")

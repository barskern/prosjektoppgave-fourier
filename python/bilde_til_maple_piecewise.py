#!/bin/env python3

# Man må installere python3.6, Pillow og numpy ved hjelp av pip install
# Altså etter man har installert python3.6 så må man skrive disse i et kommandovindu
#
# pip install Pillow
# pip install numpy
#
# Da skal det funke, hvis ikke spør meg
from PIL import Image
import numpy as np
import os
import json
import math

DATA_DIR = os.path.join(os.getcwd(), '../bilder/fourier_bilder/data/')
IMAGE_DIR = os.path.join(os.getcwd(), '../bilder/fourier_bilder/')

##########################################################################
IMAGE_DATA_NAME = "rocket_original.json" #### ENDRE PÅ DENNE FOR Å ENDRE DATA FIL
##########################################################################

def read_datafile(image_data_name):
    res_json = ""
    with open(os.path.join(DATA_DIR, image_data_name), 'r') as json_file:
        res_json = json.load(json_file)
    return res_json

def image_array_to_piecewise_metode1(np_array):
    res = "f(t) := piecewise("
    roffset = 0
    for row in np_array:
        for value in row:
            res += str(roffset) + " < t <= " + str(roffset+1) + ", " + str(value) + ", "
            roffset += 1
    res = res.strip().strip(',')
    return res + ")"

def image_array_to_piecewise_metode2(np_array):
    res = "f(t) := piecewise("
    roffset = 0
    reverse_row = False
    for row in np_array:
        altered_row = reversed(row) if reverse_row else row
        reverse_row = not reverse_row
        for value in altered_row:
            res += str(roffset) + " < t <= " + str(roffset+1) + ", " + str(value) + ", "
            roffset += 1
    res = res.strip().strip(',')
    return res + ")"


def image_array_to_piecewise_metode3(np_array):
    res = "f(t) := piecewise("
    roffset = 0
    increment_offset = 1
    x = 0
    y = 0

    res += str(roffset) + " < t <= " + str(roffset+1) + ", " + str(np_array[y][x]) + ", "
    roffset += 1

    for index in range(int(np_array.shape[0]/2)):
        for i in range(increment_offset, 0, -1):
            if(y > 0):
                y -= 1
            x += 1
            res += str(roffset) + " < t <= " + str(roffset+1) + ", " + str(np_array[y][x]) + ", "
            #print("X-loop: " + str(y) + str(x))
            roffset += 1

        increment_offset += (1 if increment_offset < np_array.shape[0]-1 else 0)

        for i in range(increment_offset, 0, -1):
            if(x > 0):
                x -= 1
            y += 1
            res += str(roffset) + " < t <= " + str(roffset+1) + ", " + str(np_array[y][x]) + ", "
            #print("Y-loop: " + str(y) + str(x))
            roffset += 1

        increment_offset += (1 if increment_offset < np_array.shape[0]-1 else 0)

    for index in range(int(np_array.shape[0]/2)):
        moved_over = False
        for i in range(increment_offset, 0, -1):
            if(y > 0 and moved_over):
                y -= 1
            moved_over = True
            x += 1
            res += str(roffset) + " < t <= " + str(roffset+1) + ", " + str(np_array[y][x]) + ", "
            #print("X-loop: " + str(y) + str(x))
            roffset += 1

        increment_offset -= 1

        moved_over = False
        for i in range(increment_offset, 0, -1):
            if(x > 0 and moved_over):
                x -= 1
            moved_over = True
            y += 1
            res += str(roffset) + " < t <= " + str(roffset+1) + ", " + str(np_array[y][x]) + ", "
            #print("Y-loop: " + str(y) + str(x))
            roffset += 1

        increment_offset -= 1

    res = res.strip().strip(',')
    return res + ")"




def main():
    image_array = read_datafile(IMAGE_DATA_NAME)
    image_np_array = np.array(image_array, np.dtype(np.uint8))
    new_image = Image.fromarray(image_np_array,'L')

    image_name = os.path.splitext(os.path.basename(IMAGE_DATA_NAME))[0] + ".png"

    with open(os.path.join(IMAGE_DIR, image_name), 'wb') as image_file:
        new_image.save(image_file, 'PNG')

    print("Lagret bilde: " + os.path.join(IMAGE_DIR, image_name))
    print("Piecewise metode 1:")
    print(image_array_to_piecewise_metode1(image_np_array))
    print("Piecewise metode 2:")
    print(image_array_to_piecewise_metode2(image_np_array))
    print("Piecewise metode 3:")
    print(image_array_to_piecewise_metode3(image_np_array))


if __name__ == '__main__':
    main()

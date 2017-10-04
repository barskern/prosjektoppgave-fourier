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
GENERATED_DIR = os.path.join(os.getcwd(), '../bilder/fourier_bilder/genererte/')

# Height and width of np_array must be divisible by 8
def array_into_eight_by_eight(np_array):
    width = np_array.shape[0]
    height = np_array.shape[1]
    if(width % 8 > 0 or height % 8 > 0):
        return None
    # Les som en bok
    array_eight_by_eights = [ [] for i in range(int(height/8)) ]
    array_eight_by_eight_col_offset = 0

    for y_matrix in range(int(width/8)):
        n1 = np.arange(8*y_matrix, 8*y_matrix+8)
        for x_matrix in range(int(height/8)):
            n2 = np.arange(8*x_matrix, 8*x_matrix+8)
            array_eight_by_eights[array_eight_by_eight_col_offset].append(np_array[n1[:,None], n2[None,:]])
        array_eight_by_eight_col_offset += 1

    return array_eight_by_eights

def assembly_array_of_eight_by_eight(array_eight_by_eights):
    rows_eight_by_eight = []
    for row_eight_by_eight in array_eight_by_eights:
        rows_eight_by_eight.append(np.concatenate(row_eight_by_eight, axis=1))
    return np.concatenate(rows_eight_by_eight, axis=0)

def numpyarray_to_image(np_array, filepath):
    new_image = Image.fromarray(np_array,'L')
    with open(filepath, 'wb') as image_file:
        new_image.save(image_file, 'PNG')

def image_to_numpyarray(loaded_image):
    converted_image_file = loaded_image.convert('L')
    return np.reshape(np.array(converted_image_file.getdata(), np.dtype(np.uint8)), (-1, converted_image_file.width))

def write_datafile(filepath, np_array):
    with open(filepath, "w") as json_file:
        json.dump(np_array.tolist(), json_file)

def read_datafile(filepath):
    res_json = ""
    with open(filepath, 'r') as json_file:
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


def test_main():
    image_data_name = "rocket_original.json"
    image_array = read_datafile(os.path.join(DATA_DIR, image_data_name))
    image_np_array = np.array(image_array, np.dtype(np.uint8))
    image_name = image_data_name.split('.')[0] + ".png"
    filepath = os.path.join(IMAGE_DIR, image_name)

    numpyarray_to_image(image_np_array, filepath)

    print("Lagret bilde: " + filepath)
    print("Piecewise metode 1:")
    print(image_array_to_piecewise_metode1(image_np_array))
    print("Piecewise metode 2:")
    print(image_array_to_piecewise_metode2(image_np_array))
    print("Piecewise metode 3:")
    print(image_array_to_piecewise_metode3(image_np_array))

def main_main():
    image_name_ext = "small_black_white_road.jpg"
    image_name = image_name_ext.split('.')[0]

    np_array = None
    with Image.open(os.path.join(IMAGE_DIR, image_name_ext)) as big_image:
        np_array = image_to_numpyarray(big_image)

    array_eight_by_eights = array_into_eight_by_eight(np_array)

    for row_index, row_eight_by_eights in enumerate(array_eight_by_eights):
        for col_index, eight_by_eight in enumerate(row_eight_by_eights):
            #####################################################################################
            # HER KAN VI LAGE EN FOURIERREKKE AV DATAEN OG GENERERE ET NYTT BILDE SOM BLE LAGET AV FOURIERREKKEN
            # Under er et eksempel på en slik endring, her en gjøre jeg bilde mørkere, bare for å vise at det funker!
            #####################################################################################
            array_eight_by_eights[row_index][col_index] = (eight_by_eight * .3).astype(np.dtype(np.uint8))
            #####################################################################################

    new_np_array = assembly_array_of_eight_by_eight(array_eight_by_eights)

    numpyarray_to_image(new_np_array, os.path.join(GENERATED_DIR, image_name + ".png"))

    write_datafile(os.path.join(DATA_DIR, image_name + ".json"), np_array)
    write_datafile(os.path.join(DATA_DIR, image_name + ".gen.json"), new_np_array)

def main():
    main_main()

if __name__ == '__main__':
    main()

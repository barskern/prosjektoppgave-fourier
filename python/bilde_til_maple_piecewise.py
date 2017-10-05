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
from math import cos

DATA_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../bilder/fourier_bilder/data/'))
IMAGE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../bilder/fourier_bilder/'))
GENERATED_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../bilder/fourier_bilder/genererte/'))
ANALYSERTE_BLOKKER_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../bilder/fourier_bilder/genererte/analyserte_blokker/'))

# Gjør om en array til en 1d array med pikselverdier. 3 ulike metoder (se "Prosjektoppgaven.mw")
def image_array_to_values_metode1(np_array):
    res = []
    for row in np_array:
        for value in row:
            res.append(value)
    return res

def values_to_image_array_metode1(value_array):
    np_array = [ [] for i in range(8) ]
    for i in range(8):
        for j in range(8):
            np_array[i].append(value_array[j + (i * 8)])

    return np.array(np_array, dtype=np.uint8)

def image_array_to_values_metode2(np_array):
    res = []
    reverse_row = False
    for row in np_array:
        altered_row = reversed(row) if reverse_row else row
        reverse_row = not reverse_row
        for value in altered_row:
            res.append(value)
    return res

def values_to_image_array_metode2(value_array):
    np_array = [ [] for i in range(8) ]
    reverse_row = False
    for i in range(8):
        for j in range(8):
            row_offset = j if not reverse_row else 7-j
            np_array[i].append(value_array[(i*8) + row_offset])
        reverse_row = not reverse_row
    return np.array(np_array, dtype=np.uint8)

def image_array_to_values_metode3(np_array):
    res = []
    increment_offset = 1
    x = 0
    y = 0

    res.append(np_array[y][x])

    for index in range(int(np_array.shape[0]/2)):
        for i in range(increment_offset, 0, -1):
            if(y > 0):
                y -= 1
            x += 1
            res.append(np_array[y][x])
            #print("X-loop: " + str(y) + str(x))

        increment_offset += (1 if increment_offset < np_array.shape[0]-1 else 0)

        for i in range(increment_offset, 0, -1):
            if(x > 0):
                x -= 1
            y += 1
            res.append(np_array[y][x])
            #print("Y-loop: " + str(y) + str(x))

        increment_offset += (1 if increment_offset < np_array.shape[0]-1 else 0)

    for index in range(int(np_array.shape[0]/2)):
        moved_over = False
        for i in range(increment_offset, 0, -1):
            if(y > 0 and moved_over):
                y -= 1
            moved_over = True
            x += 1
            res.append(np_array[y][x])
            #print("X-loop: " + str(y) + str(x))

        increment_offset -= 1

        moved_over = False
        for i in range(increment_offset, 0, -1):
            if(x > 0 and moved_over):
                x -= 1
            moved_over = True
            y += 1
            res.append(np_array[y][x])
            #print("Y-loop: " + str(y) + str(x))

        increment_offset -= 1

    return res

#####################################################################################################
# Velg om du vil generere piecewise for maple eller lage et bilde fra psi(t) funksjonen.
GENERATE_PIECEWISE_BOOL = False

# Velg indeksene for 8x8 blokken dere vil analysere! 0, 0 er den blokken øverst til venstre.
BLOCK_INDEXES = ( 11, 0 ) # VELG HVILKEN BLOKK AV 8x8 DERE VIL UNDERSØKE. (x, y)

# Skriv inn navnet på bildefilen. NB! Filen må ligge i mappen "fourier_bilder"
IMAGE_NAME = "bilde1.jpg"

# Endre denne variabelen til metoden dere ønsker. Fjern hastaggen foran metoden dere ønsker og putt en hastag forran alle metodene dere ikke vil bruke
#METHOD = image_array_to_values_metode1; REVERSE_METODE = values_to_image_array_metode1
METHOD = image_array_to_values_metode2; REVERSE_METODE = values_to_image_array_metode2
#METHOD = image_array_to_values_metode3; REVERSE_METODE = values_to_image_array_metode3 #IKKE IMPLEMENTERT TODO

# Her skrive man inn cosinusuttrykket fra maple! Sørg for at det ser riktig ut og at verdien fra cosinusuttrykket blir returnert fra funksjonen
# Bytt ut "255*cos(.4*t)" med det som kommer ut fra maple!
def psi(t):
    return 50.75000000+(-0.2836218906e-2+.6832268852*I)*exp(-(.6872233931*I)*t)+(.5263939419+.3854060212*I)*exp(-(.5890486226*I)*t)+(0.2558651562e-2+.5945059170*I)*exp(-(.4908738522*I)*t)+(.7044837111+.3936040795*I)*exp(-(.3926990818*I)*t)+(0.3003960781e-2+.2529727158*I)*exp(-(.2945243113*I)*t)+(.3003739458+.8357541753*I)*exp(-(.1963495409*I)*t)+(.3537354614+1.240596950*I)*exp(-(0.9817477044e-1*I)*t)+(.3537354656-1.240596950*I)*exp((0.9817477044e-1*I)*t)+(.3003739519-.8357541745*I)*exp((.1963495409*I)*t)+(0.3003961875e-2-.2529727125*I)*exp((.2945243113*I)*t)+(.7044837088-.3936040792*I)*exp((.3926990818*I)*t)+(0.2558654688e-2-.5945059162*I)*exp((.4908738522*I)*t)+(.5263939411-.3854060231*I)*exp((.5890486226*I)*t)+(-0.2836217344e-2-.6832268845*I)*exp((.6872233931*I)*t)

#####################################################################################################


# Lager en fourierrekke fra 8x8 blokk med term antall ledd TODO
def odd_fourierseries(eight_by_eight, method_func, reverse_method_func):
    try:
        value_array = method_func(eight_by_eight)
        T = len(value_array)
    except:
        print("Error: Vennligst velg en \"method\" funksjon.")
        return eight_by_eight

    for i in range(T):
        value_array[i] = int(psi(i))

    return reverse_method_func(value_array)

# Bredde og høyde på arrayen må være delelig på 8
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

# Gjør om en 2d array med 8x8 blokker til en stor 2d array med pikselverdier
def assembly_array_of_eight_by_eight(array_eight_by_eights):
    rows_eight_by_eight = []
    for row_eight_by_eight in array_eight_by_eights:
        rows_eight_by_eight.append(np.concatenate(row_eight_by_eight, axis=1))
    return np.concatenate(rows_eight_by_eight, axis=0)

# Gjør om en 2d array med pikselverdier til en png-bildefil
def numpyarray_to_image(np_array, filepath):
    new_image = Image.fromarray(np_array,'L')
    with open(filepath, 'wb') as image_file:
        new_image.save(image_file, 'PNG')

# Gjør om en bildefil til en 2d array med pikselverdier (bare sort/hvitt)
def image_to_numpyarray(loaded_image):
    converted_image_file = loaded_image.convert('L')
    return np.reshape(np.array(converted_image_file.getdata(), np.dtype(np.uint8)), (-1, converted_image_file.width))

# Skriver en array til en json fil
def write_datafile(filepath, np_array):
    with open(filepath, "w") as json_file:
        json.dump(np_array.tolist(), json_file)

# Leser en json fil med en 2d array
def read_datafile(filepath):
    res_json = ""
    with open(filepath, 'r') as json_file:
        res_json = json.load(json_file)
    return res_json

# Gjør om 1d array med verdier til en piecewise kommando
def array_to_piecewise(array):
    res = "f(t) := piecewise("
    roffset = 0
    for value in array:
        res += str(roffset) + " < t <= " + str(roffset+1) + ", " + str(value) + ", "
        roffset += 1
    res = res.strip().strip(',')
    return res + ")"


# En funksjon som brukes til testing av et lite bilde
def test_main():
    image_data_name = "rocket_original.json"
    image_array = read_datafile(os.path.join(DATA_DIR, image_data_name))
    image_np_array = np.array(image_array, np.dtype(np.uint8))
    image_name = image_data_name.split('.')[0] + ".png"
    filepath = os.path.join(IMAGE_DIR, image_name)

    numpyarray_to_image(image_np_array, filepath)

    print("Lagret bilde: " + filepath)
    print("Piecewise metode 1:")
    print(array_to_piecewise(image_array_to_values_metode1(image_np_array)))
    print("Piecewise metode 2:")
    print(array_to_piecewise(image_array_to_values_metode2(image_np_array)))
    print("Piecewise metode 3:")
    print(array_to_piecewise(image_array_to_values_metode3(image_np_array)))

def generate_piecewise():
    image_name = IMAGE_NAME.split('.')[0]

    np_array = None
    with Image.open(os.path.join(IMAGE_DIR, IMAGE_NAME)) as big_image:
        np_array = image_to_numpyarray(big_image)

    array_eight_by_eights = array_into_eight_by_eight(np_array)

    print("Kjoerte: " + METHOD.__name__)
    print(array_to_piecewise(METHOD(array_eight_by_eights[BLOCK_INDEXES[0]][BLOCK_INDEXES[1]])))

def generate_image_from_psi():
    image_name = IMAGE_NAME.split('.')[0]

    np_array = None
    with Image.open(os.path.join(IMAGE_DIR, IMAGE_NAME)) as big_image:
        np_array = image_to_numpyarray(big_image)

    array_eight_by_eights = array_into_eight_by_eight(np_array)

    array_eight_by_eights[BLOCK_INDEXES[0]][BLOCK_INDEXES[1]] = odd_fourierseries(array_eight_by_eights[BLOCK_INDEXES[0]][BLOCK_INDEXES[1]], METHOD, REVERSE_METODE).astype(np.dtype(np.uint8))

#    for row_index, row_eight_by_eights in enumerate(array_eight_by_eights):
#        for col_index, eight_by_eight in enumerate(row_eight_by_eights):
#            array_eight_by_eights[row_index][col_index] = (odd_fourierseries(eight_by_eight, METHOD)).astype(np.dtype(np.uint8))

#    new_np_array = assembly_array_of_eight_by_eight(array_eight_by_eights)

#    numpyarray_to_image(new_np_array, os.path.join(GENERATED_DIR, image_name + ".png"))

    numpyarray_to_image(array_eight_by_eights[BLOCK_INDEXES[0]][BLOCK_INDEXES[1]], os.path.join(ANALYSERTE_BLOKKER_DIR, image_name + "-" + str(BLOCK_INDEXES) + ".png"))

    write_datafile(os.path.join(DATA_DIR, image_name + ".json"), np_array)
#    write_datafile(os.path.join(DATA_DIR, image_name + ".gen.json"), new_np_array)

def run():
    if(GENERATE_PIECEWISE_BOOL):
        generate_piecewise()
    else:
        generate_image_from_psi()

def main():
    run()


if __name__ == '__main__':
    main()

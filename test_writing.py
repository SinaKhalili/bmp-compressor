import numpy as np
import cv2
import bitmap
import tkinter
import run_length_encoder
from tkinter import Canvas, PhotoImage, Tk

import compress_dct
from constants import *


def rgb2hex(r, g, b):
    """
    Convert an r,g,b colour to a hex code
    """
    r = r if r > 0 else 0
    g = g if g > 0 else 0
    b = b if b > 0 else 0

    r = r if r < 255 else 255
    g = g if g < 255 else 255
    b = b if b < 255 else 255

    print(r, g, b)

    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def show_image(root, width, height, pixels, row, col):
    """
    Add an image to the gui
    """
    canvas = Canvas(root, width=width, height=height)
    canvas.grid(column=col, row=row)

    img = PhotoImage(width=width, height=height)
    canvas.create_image((width / 2, height / 2), image=img, state="normal")
    canvas.image = img

    for y_index, y in enumerate(pixels):
        for x_index, x in enumerate(y):
            blue, green, red = x
            hex_code = rgb2hex(r=red, g=green, b=blue)
            img.put(hex_code, (x_index, height - y_index))


def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, "big")


def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, "big")


root = Tk()


def my_compress(filename):
    """
    Compresses to the .img format
    """
    with open("./sample_inputs/BIOS.bmp", "rb") as bmp_file:
        bmp_data = bitmap.Image(bmp_file.read())
        width = bmp_data.getBitmapWidth()
        height = bmp_data.getBitmapHeight()
        pixels = bmp_data.getPixels()

        pixels_array = np.array(pixels)
        blue, green, red = cv2.split(pixels_array)

        (
            compressed_blues,
            compressed_greens,
            compressed_reds,
        ) = compress_dct.compress_img(
            blues=blue, greens=green, reds=red, width=width, height=height
        )

        run_length_encoder.write_matrix(
            compressed_reds.astype("int8"),
            compressed_greens.astype("int8"),
            compressed_blues.astype("int8"),
            "new.img",
        )

        new_r, new_g, new_b = run_length_encoder.read_encoded_matrix("nature.img")

        pixels_array_new = compress_dct.decompress_img(new_b, new_g, new_r)

        show_image(root, width, height, pixels_array_new.astype("int16"), 1, 1)


my_compress("someting")

root.mainloop()

import bitmap
import tkinter
from tkinter import Canvas, PhotoImage, Tk


def rgb2hex(r, g, b):
    """
    Convert an r,g,b colour to a hex code
    """
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


def write_info(width, height, pixels):
    with open("test.img", "wb") as file_obj:
        file_obj.write(width.to_bytes(2, "big"))
        file_obj.write(height.to_bytes(2, "big"))

        for y_index, y in enumerate(pixels):
            for x_index, x in enumerate(y):
                blue, green, red = x
                file_obj.write(blue.to_bytes(1, "big"))
                file_obj.write(green.to_bytes(1, "big"))
                file_obj.write(red.to_bytes(1, "big"))


def read_info(root):
    with open("test.img", "rb") as file_obj:
        bytes_read = file_obj.read()

    # the first four are heigh/width
    width = int_from_bytes(bytes_read[0:2])
    height = int_from_bytes(bytes_read[2:4])

    print("Width and height are")
    print(width)
    print(height)

    pixel_bytes = bytes_read[4::]
    all_pixels = []
    for i in range(0, len(pixel_bytes) - 3, 3):
        blue = pixel_bytes[i]
        green = pixel_bytes[i + 1]
        red = pixel_bytes[i + 2]
        all_pixels.append([blue, green, red])

    k = 0
    all_pixels_2d = []
    for i in range(height):
        tmp = []
        for j in range(width):
            if k != len(all_pixels):
                tmp.append(all_pixels[k])
                k += 1

        all_pixels_2d.append(tmp)

    show_image(root, width, height, all_pixels_2d, 1, 0)


root = Tk()

with open("./sample_inputs/BIOS.bmp", "rb") as bmp_file:
    bmp_data = bitmap.Image(bmp_file.read())

    width = bmp_data.getBitmapWidth()
    height = bmp_data.getBitmapHeight()
    pixels = bmp_data.getPixels()
    print("True values:")
    print(width)
    print(height)

    write_info(width, height, pixels)
    read_info(root)

root.mainloop()

import numpy as np


def rle_encode_row(data):
    encoding = []
    prev_num = data[0]
    count = 0
    for num in data:
        if num != prev_num:
            encoding.append(count)
            encoding.append(prev_num)

            count = 1
            prev_num = num
        else:
            count += 1

    encoding.append(count)
    encoding.append(prev_num)

    return np.array(encoding)


def rle_encode_matrix(matrix):
    new_arr = []
    for row in matrix:
        new_arr.append(rle_encode_row(row))

    return new_arr


def rle_decode_matrix(matrix):
    new_arr = []
    for row in matrix:
        ans = []
        tuples = [row[i : i + 2] for i in range(0, len(row), 2)]
        for count, element in tuples:
            ans += [element] * count
        new_arr.append(ans)

    return np.array(new_arr)


def read_encoded_matrix(filename):
    width = height = None

    red = []
    green = []
    blue = []

    with open(filename, "rb") as file_obj:
        height, width = np.load(file_obj)

        for i in range(height):
            red.append(np.load(file_obj))

        for i in range(height):
            green.append(np.load(file_obj))

        for i in range(height):
            blue.append(np.load(file_obj))

    return (
        rle_decode_matrix(red),
        rle_decode_matrix(green),
        rle_decode_matrix(blue),
    )


def write_matrix(red, green, blue, filename):

    height, width = red.shape
    run_length_red = rle_encode_matrix(red)
    run_length_green = rle_encode_matrix(green)
    run_length_blue = rle_encode_matrix(blue)

    with open(filename, "wb") as file_obj:
        np.save(file_obj, np.array([height, width]))

        for row in run_length_red:
            np.save(file_obj, row.astype("int8"))

        for row in run_length_green:
            np.save(file_obj, row.astype("int8"))

        for row in run_length_blue:
            np.save(file_obj, row.astype("int8"))


def write_matrix_bytes(red, green, blue, filename):

    height, width = red.shape
    run_length_red = rle_encode_matrix(red)
    run_length_green = rle_encode_matrix(green)
    run_length_blue = rle_encode_matrix(blue)

    with open(filename, "wb") as file_obj:
        file_obj.write(width.to_bytes(2, "big"))
        file_obj.write(height.to_bytes(2, "big"))

        # for row in run_length_red:
        #     for pixel in


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

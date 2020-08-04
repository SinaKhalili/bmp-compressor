import numpy as np
import cv2
from matplotlib import pyplot as plt
from numpy.linalg import inv
import time
import sys
from constants import *


def dct_coeff():
    T = np.zeros([8, 8])
    for i in range(8):
        for j in range(8):
            if i == 0:
                T[i, j] = 1 / np.sqrt(8)
            elif i > 0:
                T[i, j] = np.sqrt(2 / 8) * np.cos((2 * j + 1) * i * np.pi / 16)
    return T


def quantization_level(n):
    Q50 = np.zeros([8, 8])

    Q50 = np.array(
        [
            [16, 11, 10, 16, 24, 40, 52, 61],
            [12, 12, 14, 19, 26, 58, 60, 55],
            [14, 13, 16, 24, 40, 57, 69, 56],
            [14, 17, 22, 29, 51, 87, 80, 62],
            [18, 22, 37, 56, 68, 109, 103, 77],
            [24, 35, 55, 64, 81, 104, 113, 92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 103, 99],
        ]
    )

    Q = np.zeros([8, 8])
    for i in range(8):
        for j in range(8):
            if n > 50:
                Q[i, j] = min(np.round((100 - n) / 50 * Q50[i, j]), 255)
            else:
                Q[i, j] = min(np.round(50 / n * Q50[i, j]), 255)
    return Q


def quantiz_div(a, b):
    tmp = np.zeros(a.shape)
    for i in range(8):
        for j in range(8):
            tmp[i, j] = np.round(a[i, j] / b[i, j])
    return tmp


def quantiz(D, Q):
    tmp = np.zeros(D.shape)
    mask = np.zeros([8, 8])
    for i in range(D.shape[0] // 8):
        for j in range(D.shape[1] // 8):
            mask = quantiz_div(D[8 * i : 8 * i + 8, 8 * j : 8 * j + 8], Q)
            tmp[8 * i : 8 * i + 8, 8 * j : 8 * j + 8] = mask
    return tmp


def decompress_mul(a, b):
    tmp = np.zeros(a.shape)
    for i in range(8):
        for j in range(8):
            tmp[i, j] = a[i, j] * b[i, j]
    return tmp


def decompress(C, Q, T, T_prime):
    R = np.zeros(C.shape)
    mask = np.zeros([8, 8])
    for i in range(C.shape[0] // 8):
        for j in range(C.shape[1] // 8):
            mask = decompress_mul(C[8 * i : 8 * i + 8, 8 * j : 8 * j + 8], Q)
            R[8 * i : 8 * i + 8, 8 * j : 8 * j + 8] = mask

    N = np.zeros(C.shape)

    for i in range(R.shape[0] // 8):
        for j in range(R.shape[1] // 8):
            mask = T_prime @ R[8 * i : 8 * i + 8, 8 * j : 8 * j + 8] @ T
            N[8 * i : 8 * i + 8, 8 * j : 8 * j + 8] = np.round(mask) + 128 * np.ones(
                [8, 8]
            )

    return N


def compress_img(blues, greens, reds, width, height):

    blues = blues - 128 * np.ones([height, width])
    greens = greens - 128 * np.ones([height, width])
    reds = reds - 128 * np.ones([height, width])

    discrete_reds = dct(reds, transform_matrix, transform_matrix_prime)
    discrete_greens = dct(greens, transform_matrix, transform_matrix_prime)
    discrete_blues = dct(blues, transform_matrix, transform_matrix_prime)

    compressed_reds = quantiz(discrete_reds, quantization_matrix)
    compressed_reds[compressed_reds == 0] = 0

    compressed_greens = quantiz(discrete_greens, quantization_matrix)
    compressed_greens[compressed_greens == 0] = 0

    compressed_blues = quantiz(discrete_blues, quantization_matrix)
    compressed_blues[compressed_blues == 0] = 0

    return compressed_blues, compressed_greens, compressed_reds


def decompress_img(compressed_blues, compressed_greens, compressed_reds):
    Q = quantization_matrix
    T = transform_matrix
    T_prime = transform_matrix_prime

    N_reds = decompress(compressed_reds, Q, T, T_prime)
    N_greens = decompress(compressed_greens, Q, T, T_prime)
    N_blues = decompress(compressed_blues, Q, T, T_prime)

    pixels_array = cv2.merge((N_blues, N_greens, N_reds))

    return pixels_array


def Evaluate(file):

    I = cv2.imread(file)

    I1 = cv2.imread("Decompressed.jpg")

    m, n, k = I1.shape

    rms = np.sqrt(np.sum(np.square(I1 - I))) / (m * n)

    snr = np.sum(np.square(I1)) / np.sum(np.square(I1 - I))

    return rms, snr


def dct(M, T, T_prime):
    dct_res = np.zeros(M.shape)
    mask = np.zeros([8, 8])
    for i in range(M.shape[0] // 8):
        for j in range(M.shape[1] // 8):
            mask = M[8 * i : 8 * i + 8, 8 * j : 8 * j + 8]
            dct_res[8 * i : 8 * i + 8, 8 * j : 8 * j + 8] = T @ mask @ T_prime

    return dct_res


if __name__ == "__main__":
    file = sys.argv[1]
    level = int(sys.argv[2])
    print("Filename: ", file)
    print("Level of compression: ", level)

    print("Compressing....")
    start = time.time()
    C_blues, C_greens, C_reds, Q, T, T_prime = Compress_img(file, level)
    time_comp = time.time()
    print("Compression Time: ", np.round(time_comp - start, 1), " sec")

    print("Decompressing...")
    Decompress_img(C_blues, C_greens, C_reds, Q, T, T_prime)
    time_decomp = time.time()

    print("Decompression Time: ", np.round(time_decomp - time_comp, 1), " sec")

    end = time.time()
    print("Total: ", np.round(end - start, 1), " sec")
    rms, snr = Evaluate(file)
    print("RMS: ", np.round(rms, 4))
    print("SNR: ", np.round(snr, 4))

# -*- coding: utf-8 -*-
import math


def find_num_of_digits(num, radix):
    # 1023 = 2**10-1
    return math.ceil(math.log(num + 1, radix))


def num2digits(num, radix, num_of_digits, order="big-endian"):
    # 以radix为基数，数n需要多少位表示
    # 2**4-1 == 15 == 1111 10000 == 16
    necessary_num_of_digits = math.ceil(math.log(num + 1, radix))
    if num_of_digits < necessary_num_of_digits:
        raise Exception('指定位数不足！')
    digits = []
    if order == "big-endian":
        for i in range(num_of_digits, 0, -1):
            digit = num // radix ** (i - 1) % radix
            digits.append(digit)
    if order == "small-endian":
        for i in range(1, num_of_digits + 1):
            digit = num % radix ** (i) // radix ** (i - 1)
            digits.append(digit)
    return digits


def digits2num(digits, radix, order="big-endian"):
    if order == "big-endian":
        digits.reverse()
    '''
    num = 0
    for i, digit in enumerate(digits):
        num += digit*radix**i
    '''
    num = 0
    power = 1
    for i, digit in enumerate(digits):
        num += digit * power
        power *= radix
    return num




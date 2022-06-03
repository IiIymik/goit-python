import time
from multiprocessing import Pool


def list_number_factorize(number):
    return [num for num in range(1, number + 1) if number % num == 0]


def factorize(*numbers):
    return list_number_factorize(*numbers)


if __name__ == "__main__":
    start = time.time()

    with Pool(4) as executor:
        # a, b, c, d = executor.map(factorize, (128, 255, 99999, 10651060))
        a, b, c, d = executor.map(factorize, (45403940, 34534334, 23434432, 73423424))

    end = time.time()
    print(end-start)

    # assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    # assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    # assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    # assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
    #              380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    assert a == [1, 2, 4, 5, 10, 17, 20, 34, 68, 85, 170, 340, 133541, 267082, 534164, 667705, 1335410,
                 2270197, 2670820, 4540394, 9080788, 11350985, 22701970, 45403940]
    assert b == [1, 2, 2477, 4954, 6971, 13942, 17267167, 34534334]
    assert c == [1, 2, 4, 7, 8, 14, 16, 17, 28, 32, 34, 56, 64, 68, 112, 119, 136, 181, 224, 238, 272, 289, 362, 448,
                 476, 544, 578, 724, 952, 1088, 1156, 1267, 1448, 1904, 2023, 2312, 2534, 2896, 3077, 3808, 4046,
                 4624, 5068, 5792, 6154, 7616, 8092, 9248, 10136, 11584, 12308, 16184, 18496, 20272, 21539, 24616,
                 32368, 40544, 43078, 49232, 52309, 64736, 81088, 86156, 98464, 104618, 129472, 172312, 196928,
                 209236, 344624, 366163, 418472, 689248, 732326, 836944, 1378496, 1464652, 1673888, 2929304, 3347776,
                 5858608, 11717216, 23434432]
    assert d == [1, 2, 4, 8, 16, 32, 64, 67, 134, 268, 536, 1072, 2144, 4288, 17123, 34246, 68492, 136984, 273968,
                 547936, 1095872, 1147241, 2294482, 4588964, 9177928, 18355856, 36711712, 73423424]

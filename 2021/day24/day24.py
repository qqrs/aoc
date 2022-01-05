A = [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1]
B = [10, 14, 14, -13, 10, -13, -7, 11, 10, 13, -4, -9, -13, -9]
C = [2, 13, 13, 9, 15, 3, 6, 5, 16, 1, 6, 3, 7, 9]
PARAMS = zip(A, B, C)


def check_modelnum(modelnum):
    digits = [int(v) for v in str(modelnum)]
    assert(len(digits) == 14)
    assert(all(v >= 1 and v <= 9 for v in digits))

    z = []
    for w, (a, b, c) in zip(digits, PARAMS):
        if not a:
            z.append(w + c)
        else:
            if w != z.pop() + b:
                print('w != z.pop() + b  w={} b={}'.format(w,b))
                return False

        print('{}: {}'.format(a, z))

    return True


# def check_digit(w, z, a, b, c):
    # x = (z % 26) + b
    # if a:
        # z /= 26

    # if x != w:
        # z *= 26

    # y = x * (w + c)
    # z += y
    # return z


# def check_modelnum(modelnum):
    # digits = [int(v) for v in str(modelnum)]
    # if len(digits) != 14:
        # return False
    # if not all(v >= 1 and v <= 9 for v in digits):
        # return False

    # z = 0
    # for digit, params in zip(digits, PARAMS):
        # z = check_digit(digit, z, *params)
        # print(z)

    # if z == 0:
        # return True
    # else:
        # return False


def main():
    # m = 99999999999999
    # m = 93997999296912
    m = 81111379141811
    check_modelnum(m)
    return


def getparams():
    print((
    C[0] + B[13],
    C[1] + B[6]   ,
    C[2] + B[3]   ,
    C[4] + B[5]   ,
    C[7] + B[12] ,
    C[8] + B[11] ,
    C[9] + B[10] ))


if __name__ == '__main__':
    # getparams()
    main()

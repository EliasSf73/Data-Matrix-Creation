# -------------------------------------------------------
# TODO: Import libraries if required
# Do not change the names and parameters of the functions
# -------------------------------------------------------

###ECC
"""
Do NOT modify this file
for KAIST CS101 Homework 3, Fall 2022.
* Author: Younggeol Cho (rangewing@kaist.ac.kr)
"""

_MODULO_VALUE = 0x12D
_LOG = [0] * 256
_ALOG = [0] * 255
_POLY = [62, 111, 15, 48, 228]
_N_ORDER = len(_POLY)
_ECC_INITIALIZED = False


def _init_ecc():
    global _ECC_INITIALIZED
    p = 1
    for i in range(255):
        _ALOG[i] = p
        _LOG[p] = i
        p *= 2
        if (p >= 256):
            p ^= _MODULO_VALUE
    _ECC_INITIALIZED = True


def ecc(word):
    """
        Generate a Reed-Solomon error correction code of length 5

        Args:
            word: A list of three integers (e.g., [90, 84, 76])

        Returns:
            res: Reed-Solomon error correction code (e.g., [82, 141, 198, 154, 160])
    """
    if not _ECC_INITIALIZED: _init_ecc()
    if type(word) is not list:
        raise ValueError(f'Argument should be an integer list of length 3, but it is a(n) {type(word)}.')
    if len(word) != 3:
        raise ValueError(f'Argument should be an integer list of length 3, but its length is {len(word)}.')
    for e in word:
        if type(e) is not int:
            raise ValueError(
                f'Argument should be an integer list of length 3, but the list has an element of type {type(e)}.')

    res = [0] * _N_ORDER
    for c in word:
        m = res[0] ^ c
        for k in range(_N_ORDER - 1):
            res[k] = (res[k + 1] ^ _ALOG[(_LOG[m] + _LOG[_POLY[k]]) % 255]) if m != 0 else res[k + 1]
        res[_N_ORDER - 1] = _ALOG[(_LOG[m] + _LOG[_POLY[_N_ORDER - 1]]) % 255] if m != 0 else 0
    return res


_init_ecc()


###HOMEWORK

from cs101_hw3 import ecc

"""
Task 1. Data encoding

Do NOT modify the function names 
"""


def str_to_list(input_string):
    """
    Task 1.1
        Convert a given string to a list of integers.
        Each element of the list should be 1 + (ASCII code number) of the corresponding character in the string.

        Args:
            input_string: An alphanumeric string to be encoded
        Returns:
            A list of three integers
    """
    # --------------------
    # TODO: Implement here
    # --------------------
    # l = []
    input_string = input_string + " " * 3
    # while len(input_string) < 3:
    #     input_string += " "

    # if len(input_string) > 3:
    # input_string = input_string[:3]

    l = [ord(x) + 1 for x in input_string[:3]]

    # for x in input_string:
    #     l.append( ord(x) + 1 )

    return l


def append_ecc(int_list):
    """
    Task 1.2
        Append a Reed-Solomon Error Correction Code (ECC) at the end of the integer list.

        Args:
            int_list: A list of three integers
        Returns:
            A list of eight integers with a Reed-Solomon ECC
    """
    # --------------------
    # TODO: Implement here
    # --------------------
    x = ecc(int_list)
    int_list.extend(x)
    return int_list


def list_to_binary(int_list):
    """
    Task 1.3
        Convert the integer list with ECC to the binary data list, a list of 8-bit binary tuple.

        Args:
            int_list: A list of eight integers with a Reed-Solomon ECC
        Returns:
            A binary data list, a list of eight 8-bit binary tuples
    """
    # --------------------
    # TODO: Implement here
    # --------------------
    nl = []
    for a in int_list:

        c = list(bin(a)[2:])
        while len(c) < 8:
            c = [0] + c
        for i in range(len(c)):
            c[i] = int(c[i])
        nl.append(tuple(c))
    return nl


def main():
    """
        main() will not used when grading
    """
    input_string = input('Input a string to encode: ')
    int_list = str_to_list(input_string)
    print(f'[(1) str_to_list] -> {int_list}')

    int_list_with_ecc = append_ecc(int_list)
    print(f'[(2) append_ecc]  -> {int_list_with_ecc}')

    binary_data = list_to_binary(int_list_with_ecc)
    print(f'=> Encoded binary data: {binary_data}')


if __name__ == '__main__':
    """ Do NOT modify here """
    main()


##TASK2

TODO: Import
libraries if required


# Do not change the names and parameters of the functions
# -------------------------------------------------------

def str_to_list(input_string):
    """
    Task 1.1
        Args:
            input_string
        Returns:
            List
    """
    # ------------------------------------
    # TODO: Copy-and-paste from Task 1.1
    # ------------------------------------

    input_string = input_string + " " * 3
    l = [ord(x) + 1 for x in input_string[:3]]
    return l


def append_ecc(int_list):
    """
    Task 1.2
        Args:
            input_string
        Returns:
            List
    """
    # ------------------------------------
    # TODO: Copy-and-paste from Task 1.2
    # ------------------------------------
    x = ecc(int_list)
    int_list.extend(x)
    return int_list


def list_to_binary(int_list):
    """
    Task 1.3
        Args:
            input_string
        Returns:
            List
    """
    # ------------------------------------
    # TODO: Copy-and-paste from Task 1.3
    # ------------------------------------
    nl = []
    for a in int_list:

        c = list(bin(a)[2:])
        while len(c) < 8:
            c = [0] + c
        for i in range(len(c)):
            c[i] = int(c[i])
        nl.append(tuple(c))
    return nl


def place_block(img, binary_data, position):
    """
    Task 2.1
        Place a data block represented in a 8-bit binary tuple at the specified position (x, y) on the image

        Args:
            img: A 10x10 cs1media image object
            binary_data: A 8-bit binary tuple
            position: A coordinate tuple (x, y)
        Returns:
            A 10x10 cs1media image object with the data block placed
    """

    img_with_block = img

    # --------------------
    # TODO: Implement here
    # --------------------
    list_binary = list(binary_data)
    list_binary.insert(2, 0)
    for i in range(len(list_binary)):
        change_pos = (i % 3, i // 3)
        target_x = change_pos[0] + position[0]
        target_y = change_pos[1] + position[1]
        if target_x > 8:
            target_x = target_x % 8
        if target_y > 8:
            target_y = target_y % 8
        col = [(255, 255, 255), (0, 0, 0)][list_binary[i]]
        if not i == 2:
            img_with_block.set(target_x, target_y, col)

    return img_with_block


def create_data_matrix(input_string):
    """
    Task 2.2
        Convert the given string into a 10x10 Data matrix

        Args:
            input_string: An alphanumeric string to encode
        Returns:
            A 10x10 Data matrix image
    """

    data_matrix = create_picture(10, 10, color=(255, 255, 255))

    # --------------------
    # TODO: Implement here
    # --------------------
    position_map = ((7, 3), (1, 1), (3, 7), (6, 8), (4, 2), (2, 4), (8, 6), (5, 5))
    len3 = str_to_list(input_string)
    len8 = append_ecc(len3)
    block_map = list_to_binary(len8)
    for i in range(len(position_map)):
        data_matrix = place_block(data_matrix, block_map[i], position_map[i])
    for x in range(10):
        for y in range(10):
            if x == 0 or y == 9:
                data_matrix.set(x, y, (0, 0, 0))
            if x == 9 or y == 0:
                if (x + y) % 2 == 0:
                    data_matrix.set(x, y, (0, 0, 0))

    return data_matrix


def main():
    """
        main() will not used in grading
    """

    task_number = 1  # set this to 2 to test Task 2.2

    # Task 2.1
    if task_number == 1:
        img = create_picture(10, 10, color=(255, 255, 255))
        img_with_block = place_block(img, binary_data=(0, 1, 1, 0, 1, 1, 0, 1), position=(7, 3))
        img_with_block = place_block(img_with_block, binary_data=(0, 1, 0, 1, 0, 1, 0, 0), position=(5, 5))
        img_with_block.show()

    # Task 2.2
    elif task_number == 2:
        input_string = input('Input a string to encode: ')
        input_string = 'SoC'
        data_matrix = create_data_matrix(input_string)
        data_matrix.show()


if __name__ == '__main__':
    """ Do NOT modify here """
    main()
#TASK3

# TODO: Import libraries if required
# Do not change the names and parameters of the functions
# -------------------------------------------------------

def read_data_block(data_matrix, position):
    """
    Task 3.1
       Read a data block at position (x, y) on img

        Args:
            data_matrix: A 10x10 Data matrix image (cs1media object)
            position: A coordinate tuple (x, y)
        Returns:
            A 8-bit binary tuple
    """
    # --------------------
    # TODO: Implement here
    # --------------------

    output = [0, 0, 0, 0, 0, 0, 0, 0]
    pos = ((0, 0), (1, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2))
    for i in range(len(pos)):
        target_x = pos[i][0] + position[0]
        target_y = pos[i][1] + position[1]
        if target_x > 8:
            target_x = target_x % 8
        if target_y > 8:
            target_y = target_y % 8
        output[i] = int(1 - data_matrix.get(target_x, target_y)[0] / 255)
    return tuple(output)


def read_data_matrix(data_matrix):
    """
    Task 3.2
        Decode a given Data matrix into string

        Args:
            data_matrix: A 10x10 Data matrix image (cs1media object)
        Returns:
            A decoded string
    """
    # --------------------
    # TODO: Implement here
    # --------------------
    string = '' * 3
    binary = [0] * 8
    position_map = ((7, 3), (1, 1), (3, 7), (6, 8), (4, 2), (2, 4), (8, 6), (5, 5))
    tup = ()
    for i in range(len(position_map)):
        binary[i] = read_data_block(data_matrix, (position_map[i][0], position_map[i][1]))
    x = binary[:3]

    string = ''
    for i in x:
        hahah = ''.join(map(str, i))  # map - maps type to every input in x[0] and join converts list to str
        decimal = int(hahah, 2)
        string += chr(decimal - 1)
    return string


def main():
    """
        main() will not used when grading
    """
    data_matrix = load_picture('examples/SoC.png')
    data_block = read_data_block(data_matrix, (7, 3))
    print(f'Data block = {data_block}')

    decoded_string = read_data_matrix(data_matrix)
    print(f'Decoded string = {decoded_string}')


if __name__ == '__main__':
    """ Do NOT modify here """
    main()
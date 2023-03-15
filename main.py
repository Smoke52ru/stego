import os
from PIL import Image


def decrypt(path_to_image):
    """
    :param path_to_image:
    :return: decrypted text
    """

    image_obj = Image.open(path_to_image)
    width = image_obj.size[0]
    height = image_obj.size[1]
    image_pixels = image_obj.load()

    cur_x, cur_y = 0, 0
    full_code = ''

    # parse code from pixels
    i = 0
    while i < width * height:
        colors = image_pixels[cur_x, cur_y]

        for color in colors:
            # двоичный код без префикса '0b'
            color_code: str = '0' + format(color, "b")

            full_code += color_code[-2] + color_code[-1]

        if cur_x < (width - 1):
            cur_x += 1
        else:
            cur_y += 1
            cur_x = 0

        i += 1

    # decoding
    decoded_text = ''
    for pos in range(0, len(full_code), 8):
        code_of_symbol = full_code[pos:pos+8]
        decoded_text += chr(int(code_of_symbol, 2))

    # output
    out_filename = f'{path_to_image[:-4]}.txt'
    out_directory = 'out'
    out_fullpath = f'{out_directory}/{out_filename}'

    os.makedirs(out_directory, exist_ok=True)

    file = open(out_fullpath, "w")
    file.write(
        f'file dimensions: w - {width}px, h - {height}px\n' + 
        f'{decoded_text}'
    )
    file.close()

    print(f"Data saved in {out_fullpath}")

    return decoded_text


if __name__ == '__main__':
    filename = input("Введите название файла:\t")
    decrypt(filename)

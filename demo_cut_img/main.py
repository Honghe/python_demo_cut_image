import os

from PIL import Image


def crop(fpath):
    dir = os.path.dirname(os.path.abspath(fpath))
    fname, fext = os.path.splitext(os.path.basename(fpath))
    fname_cut = fname + '_cut' + fext
    fname_cut_color = fname + '_cut_color' + fext
    fpath_cut = os.path.join(dir, fname_cut)
    fpath_cut_color = os.path.join(dir, fname_cut_color)

    img = Image.open(fpath)
    print(img.size)  # fixed, such as (980, 16384)
    margin_x = 100
    margin_y = 45
    # 切除两边
    cropped = img.crop((0 + margin_x, 0, img.size[0] - margin_x, img.size[1] - margin_y))  # (left, upper, right, lower)
    cropped.save(fpath_cut)
    # 切除底部的白色
    cropped = cut_white(cropped)
    cropped.save(fpath_cut_color)


def most_frequent_colour(image):
    '''
    计算主要颜色
    :param image:
    :return:
    '''
    w, h = image.size
    pixels = image.getcolors(w * h)

    most_frequent_pixel = pixels[0]

    for count, colour in pixels:
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, colour)
    return most_frequent_pixel[0] / (w * h), most_frequent_pixel[1]


def cut_white(image):
    step = 100
    white_color = (255, 255, 255, 255)
    threshold = 0.99  # 即粗略认为只有一行是非白色
    # 从图片底部往上截
    while True:
        most_frequent_pixel = most_frequent_colour(image.crop((0, image.size[1] - step, image.size[0], image.size[1])))
        print(f'most_frequent_pixel {most_frequent_pixel}')
        if most_frequent_pixel[1] == white_color and most_frequent_pixel[0] > threshold:
            image = image.crop((0, 0, image.size[0], image.size[1] - step))
        else:
            break
    print('cut out: {}'.format(image.size))
    return image


if __name__ == "__main__":
    fpath = '../data/demo.png'
    crop(fpath)

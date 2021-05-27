import os
from pygame import image


def load_images():
    images = {}
    names = os.listdir('pics')
    for name in names:
        filename = os.path.join('pics', name)
        if not os.path.isfile(filename):
            print(f"Нет файла {filename}!")
            return
        print(f'{filename} loaded.')
        key, *other = name.split('.')
        images[key] = image.load(filename)
    return images


images = load_images()

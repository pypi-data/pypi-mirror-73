import requests

from pathlib import Path

from PIL import Image


def local_dir(name):
    cwd = Path.cwd()
    img_dir = cwd / name
    if not img_dir.exists():
        raise Exception(f'Create the `{name}` folder and try again')
    return img_dir


def get_image(url):
    response = requests.get(url, stream=True)
    response.raw.decode_content = True
    image = response.raw
    return image


def shrink_image(url, img_dir, max_size=960):
    size = max_size, max_size
    filename = url.split("/")[-1]
    image = Image.open(get_image(url))
    image.thumbnail(size)
    save_dir = local_dir(img_dir)
    image.save(save_dir / filename)
    return filename

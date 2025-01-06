import PIL
import PIL.Image
import os
import hashlib


def get_last_modification(file):
    """get time of last modification of passed file

    Args:
        file (str): absolute path of file
    """
    if file is not None:
        if os.path.exists(file):
            return os.stat(file).st_mtime
        else:
            return None
    else:
        return None


def get_smallest_image(directory):
    """Based on a directory with images return the smallest horizontal image

    Args:
        directory (str): Path containing images

    Returns:
        str: Absolute file path
    """
    img_list = [directory + file for file in os.listdir(directory)]
    size_sorted = sorted(img_list, key=os.path.getsize)

    landscape_imgs = []
    portrait_imgs = []
    for image in size_sorted:
        try:
            img = PIL.Image.open(image)
            if img.size[0] > img.size[1]:
                landscape_imgs.append(image)
            if img.size[0] < img.size[1]:
                portrait_imgs.append(image)
        except PIL.UnidentifiedImageError:
            # ignore unsupported formats
            pass

    if landscape_imgs:
        return landscape_imgs[0]

    if portrait_imgs:
        return portrait_imgs[0]

    # pass list so caller knows we couldn't find a compatible format
    return size_sorted


def get_file_sha1(file_path):
    if file_path is not None:
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb") as f:
                    data = f.read()
                    file_sha1 = hashlib.sha1(data).hexdigest()
                    return file_sha1
            except Exception as e:
                print(f"Error:\n{e}")

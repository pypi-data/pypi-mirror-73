from PIL import Image, ImageFont, ImageDraw, ImageFilter
from io import BytesIO


def resize_img(img):
    """
    重新剪裁图片尺寸
    :param img:
    :return: Image对象
    """
    (x, y) = img.size  # read image size
    x_s = 250  # define standard width
    y_s = int(y * x_s / x)  # calc height based on standard width
    out = img.resize((x_s, y_s), Image.ANTIALIAS)  # resize image with high-quality
    return out
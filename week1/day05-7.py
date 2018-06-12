from PIL import Image, ImageFilter
from io import BytesIO
from pytesseract import image_to_string

import requests


def main():
    img = Image.open(open('guido.jpg', 'rb'))
    # 滤镜
    img1 = img.filter(ImageFilter.GaussianBlur)
    img1.save(open('guido2.jpg', 'wb'))

    photo = Image.open(open('xixihha.jpg'), 'rb')
    photo1 = photo.point(lambda x: 0 if x < 128 else 255)
    photo1.save(open('xixihha.jpg'), 'wb')
    print(image_to_string(photo1))

    resp = requests.get('')
    img3 = Image.open(BytesIO(resp.content))
    img3.save('hello.jpg')
    print(image_to_string(img3))


if __name__ == '__main__':
    main()



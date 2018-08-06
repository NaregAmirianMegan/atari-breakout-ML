import numpy as np
from PIL import Image

def preprocess(img):
    #greyscale
    img = np.asarray(Image.open(img))
    img = np.mean(img, axis=2).astype(np.uint8)

    #resize
    img = img[::2, ::2]

    return img

def saveImgToView(img):
    im = Image.fromarray(np.uint8(img))
    im.save('images/out.jpeg')


saveImgToView(preprocess('images/image0.jpeg'))

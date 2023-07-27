import requests
import numpy as np
import cv2 as cv
# from PIL import Image
import io

i = 0

while True:
    r = requests.get("http://192.168.4.1:80/capture")
    # r = requests.get("http://192.168.4.1:81/stream")

    # print(r)

    # image = Image.open(io.BytesIO(r.content))
    # Save image to BytesIO object
    # byte_arr = io.BytesIO()
    # image.save("aaa.jpg", format='JPEG')
    # image.show()

    image = np.asarray(bytearray(r.content), dtype=np.uint8)
    cv_image = cv.imdecode(image, cv.IMREAD_COLOR)
    cv.imshow('image', cv_image)
    cv.waitKey(1)
    #print(cv_image.shape)
    
    i += 1
    if i > 1000: break

"""
file = open("capture.jpg", "wb")
file.write(r.content)
file.close()
print("Photo prise")
"""
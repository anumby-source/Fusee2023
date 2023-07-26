from flask import Flask, Response
from collections import OrderedDict
import cv2
import requests
import numpy as np

app = Flask(__name__)

url = "http://monserveurweb.com/chemin/vers/image.jpg"  # Remplacez ceci par l'URL de votre image

# Paramètres du cache
cache = OrderedDict()
cache_size = 10


def get_image(url):
    if url in cache:
        # Si l'image est dans le cache, utilisez celle-ci
        return cache[url]

    # Sinon, récupérez l'image du serveur
    response = requests.get(url)
    response.raise_for_status()  # s'assurer que la requête a réussi

    # Convertir la réponse en tableau d'octets et puis en image
    array = np.frombuffer(response.content, dtype=np.uint8)
    image = cv2.imdecode(array, flags=cv2.IMREAD_COLOR)

    # Ajouter l'image au cache
    cache[url] = image

    # Si le cache est plein, supprimez l'image la moins récemment utilisée
    if len(cache) > cache_size:
        cache.popitem(last=False)

    return image


def generate():
    while True:
        image = get_image(url)

        # Encode the image in JPEG format
        (flag, encodedImage) = cv2.imencode(".jpg", image)

        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)


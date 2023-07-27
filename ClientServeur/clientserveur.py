from flask import Flask, Response
from collections import OrderedDict
import cv2
import requests
import numpy as np
import logging

app = Flask(__name__)

url = "http://192.168.4.1:80/capture"  # Remplacez ceci par l'URL de votre image

# Paramètres du cache
cache = OrderedDict()
cache_size = 10


def generate_frames():
    # récupérez l'image du serveur
    logging.debug("getting image from server")
    response = requests.get(url)
    response.raise_for_status()  # s'assurer que la requête a réussi
    logging.debug("got image")

    # Convertir la réponse en tableau d'octets et puis en image
    array = np.frombuffer(response.content, dtype=np.uint8)
    image = cv2.imdecode(array, flags=cv2.IMREAD_COLOR)
    
    ret, buffer = cv2.imencode(".jpg", image)
    frame = buffer.tobytes()
    yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)


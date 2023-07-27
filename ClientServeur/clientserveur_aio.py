from aiohttp import web
import aiohttp
import asyncio
import cv2
import numpy as np
import logging

async def fetch(session, url):
    async with session.get(url) as response:
        logging.debug("getting image from server")
        content = await response.read()
        logging.debug("got image")

        return content

async def stream(request):
    url = "http://192.168.4.1:80/capture"  # Replace this with the URL of your image

    async def generate():
        while True:
            async with aiohttp.ClientSession() as session:
                content = await fetch(session, url)
                
            array = np.frombuffer(content, dtype=np.uint8)
            image = cv2.imdecode(array, flags=cv2.IMREAD_COLOR)

            (flag, encodedImage) = cv2.imencode(".jpg", image)
            frame = encodedImage.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return web.Response(body=generate(), content_type='multipart/x-mixed-replace; boundary=frame')

app = web.Application()
app.router.add_get('/video_feed', stream)

if __name__ == '__main__':
    web.run_app(app, host='192.168.4.2', port='5000')
    
# sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT



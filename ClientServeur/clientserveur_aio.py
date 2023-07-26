from aiohttp import web
import aiohttp
import asyncio
import cv2
import numpy as np

# Cache parameters
cache = {}
cache_size = 10

async def fetch(session, url):
    # Use cache if available
    if url in cache:
        return cache[url]

    async with session.get(url) as response:
        content = await response.read()
        # Store the content in the cache
        cache[url] = content

        # If the cache is full, remove the oldest item
        if len(cache) > cache_size:
            oldest_key = next(iter(cache))
            del cache[oldest_key]

        return content

async def stream(request):
    url = "http://monserveurweb.com/chemin/vers/image.jpg"  # Replace this with the URL of your image

    async def generate():
        while True:
            async with aiohttp.ClientSession() as session:
                content = await fetch(session, url)

            array = np.fromstring(content, dtype=np.uint8)
            image = cv2.imdecode(array, flags=cv2.IMREAD_COLOR)

            (flag, encodedImage) = cv2.imencode(".jpg", image)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

    return web.Response(body=generate(), content_type='multipart/x-mixed-replace; boundary=frame')

app = web.Application()
app.router.add_get('/video_feed', stream)

if __name__ == '__main__':
    web.run_app(app)

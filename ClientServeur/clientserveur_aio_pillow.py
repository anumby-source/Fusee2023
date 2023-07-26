from aiohttp import web
import aiohttp
import asyncio
from PIL import Image
import io

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
    url = "http://monserveurweb.com/chemin/vers/image.jpg" # Replace this with the URL of your image

    async def generate():
        while True:
            async with aiohttp.ClientSession() as session:
                content = await fetch(session, url)

            # Open image with Pillow

            image = Image.open(io.BytesIO(content))
            # Save image to BytesIO object
            byte_arr = io.BytesIO()
            image.save(byte_arr, format='JPEG')
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + byte_arr.getvalue() + b'\r\n')

    return web.Response(body=generate(), content_type='multipart/x-mixed-replace; boundary=frame')

app = web.Application()
app.router.add_get('/video_feed', stream)

if __name__ == '__main__':
    web.run_app(app)
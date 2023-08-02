#!/usr/bin/python3

from aiohttp import web
import aiohttp
import asyncio

i = 0

async def stream(request):
    async def generate():
        while True:
            global i
            texte = "texte {}".format(i)
            i += 1
            frame = texte.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return web.Response(body=generate(), content_type='multipart/x-mixed-replace; boundary=frame')

app = web.Application()
app.router.add_get('/video_feed', stream)

if __name__ == '__main__':
    try:
        web.run_app(app, host='192.168.4.3', port='5000')
    except:
        print("cannot start the routeur")
    
# sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT



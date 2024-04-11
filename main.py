import openziti
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import asyncio
from sse_starlette.sse import EventSourceResponse

from hypercorn.config import Config
from hypercorn.asyncio import serve
import signal
import cv2 as cv
import base64
import sys

shutdown_event = asyncio.Event()

# for hypercorn
address = "localhost"
port = 8443
video_file = "lambs-and-cat.mp4" #change to local file
identity = "./predalert_server2.json"
service_name = "predalert_service_2"

config = Config()
config.bind = [f"{address}:{port}"]
config.errorlog = "-" #stderr
config.loglevel = "DEBUG"

# Point these variables to  SSL cert/key files for HTTP/2 in hypercorn,
# which is necessary to support more than 6 concurrent SSE connections per domain
# config.certfile = "ssl_cert.pem"
# config.keyfile = "ssl_key.pem"


app = FastAPI()


@app.get("/")
async def indexpage(request: Request):
    html_content = """
    <html>
        <head>
            <style>
                #numbers {
                    background-color: black;
                    color:white;
                    height:600px;
                    overflow-x: hidden;
                    overflow-y: auto;
                    text-align: left;
                    padding-left:10px;
                }
            </style>
        </head>

        <body>

            <h1>Numbers:</h1>
            <div id="numbers">
            </div>
            <script>
                var source = new EventSource("/stream-sse");
                source.onmessage = function(event) {
                    document.getElementById("numbers").innerHTML += event.data + "<br>";
                };
            </script>

        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


async def text_message_generator(request):
    for number in range(1, 256 + 1):
        if await request.is_disconnected():
            print("client disconnected!!!")
            break
        yield number
        await asyncio.sleep(0.1)


@app.get('/stream-sse')
async def text_message_stream(request: Request):
    event_generator = text_message_generator(request)
    return EventSourceResponse(event_generator)


@app.get("/video")
async def videopage(request: Request):
    html_content = """
    <html>
        <head>
            <title>SSE Image Streaming</title>
        </head>

        <body>
            <img id="image" src="#" alt="Streamed Image" >
            <script>
                const imageElement = document.getElementById('image');
                const eventSource = new EventSource('/vid-stream-sse'); // Replace '/stream' with your SSE endpoint

                eventSource.onmessage = function(event) {
                    const imageData = event.data;
                    imageElement.src = 'data:image/webp;base64,' + imageData; // Change datatype if necessary, always ;base64
                };

                eventSource.onerror = function(error) {
                    console.error('EventSource failed:', error);
                    eventSource.close();
                };
            </script>

        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


async def vid_message_generator(request: Request):
    stream = cv.VideoCapture(video_file)
    # loop over frames
    while True:
        if await request.is_disconnected():
            print("client disconnected!!!")
            break
        # read frame from provided source
        (ret, frame) = stream.read()

        # break if video is done
        if not ret:
            break

        # handle JPEG encoding
        _ , image = cv.imencode(".webp", frame)

        # encode jpeg to base64 string in utf-8 format
        base64_image = base64.b64encode(image).decode("utf-8")

        yield base64_image
        await asyncio.sleep(0.001)


@app.get('/vid-stream-sse')
async def vid_message_stream(request: Request):
    event_generator = vid_message_generator(request)
    return EventSourceResponse(event_generator)


def _signal_handler(*_: any) -> None:
    shutdown_event.set()


@openziti.zitify(bindings={
    (address, port): {
        'ztx': identity, 'service': service_name}
    })
def run_webapp():
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, _signal_handler)
    loop.run_until_complete(
        serve(app, config, shutdown_trigger=shutdown_event.wait)
    )


if __name__ == "__main__":

    run_webapp()

# This file is part of ziti-streaming-webapp
# Copyright (c) 2024 Jacob Dybvald Ludvigsen (contributions@ingeniorskap.no)
# SPDX-License-Identifier: AGPL-3.0-or-later

import openziti
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import asyncio
from sse_starlette.sse import EventSourceResponse

from hypercorn.config import Config
from hypercorn.asyncio import serve
import signal
import tomllib

import ziti_streaming_webapp.webconfig

shutdown_event = asyncio.Event()


# Load configuration file
try:
    with open("./config.toml", "rb") as f:
        config_file = tomllib.load(f)
except tomllib.TOMLDecodeError as e:
    print(f"ERR: Config file couldn't load due to error: {e}")

# for hypercorn
address = config_file["ziti"]["address"]
port = config_file["ziti"]["port"]
config = Config()
config.bind = [f"{address}:{port}"]
config.errorlog = "-"  # stderr
config.loglevel = "DEBUG"

if config_file["SSL"]["enabled"]:
    config.certfile = config_file["SSL"]["certfile"]
    config.keyfile = config_file["SSL"]["keyfile"]

web_config = ziti_streaming_webapp.webconfig.webConfigHolder()

app = FastAPI()

# for ziti
identity = config_file["ziti"]["identity"]
service_name = config_file["ziti"]["service"]


@app.get("/")
async def indexpage(request: Request):
    """
    serve up index content, showing a number stream using SSE
    """
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
    """
    Produce output that will be piped to /stream-sse
    """
    for number in range(1, 256 + 1):
        if await request.is_disconnected():
            print("client disconnected!!!")
            break
        yield number
        await asyncio.sleep(0.1)


@app.get('/stream-sse')
async def text_message_stream(request: Request):
    """
    serve up the number eventSource / SSE source for client
    """
    event_generator = text_message_generator(request)
    return EventSourceResponse(event_generator)


@app.get("/video")
async def videopage(request: Request):
    """
    serve up a page using SSE for live webcam stream
    """
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
    """
    generate images to be sent to client via SSE
    """
    q_img = web_config.read_key("q_img")
    pipe_img_recv = web_config.read_key("pipe_img_recv")

    # loop over frames
    while True:
        if await request.is_disconnected():
            print("client disconnected!!!")
            break

        # retrieve image from frame_producer_process
        try:
            base64_image = q_img.get()
        except Exception as e:
            print(f"couldn't get img from q due to: {e}")
        else:
            yield base64_image

        try:
            base64_image = pipe_img_recv.recv()
        except Exception as e:
            print(f"couldn't get img from pipe due to: {e}")
        else:
            yield base64_image

        await asyncio.sleep(0.001)


@app.get('/vid-stream-sse')
async def vid_message_stream(request: Request):
    """
    serve up the video eventSource / SSE source for client
    """
    event_generator = vid_message_generator(request)
    return EventSourceResponse(event_generator)


def _signal_handler(*_: any) -> None:
    """
    gracefully terminate the app upon recieving SIGTERM
    """
    shutdown_event.set()


@openziti.zitify(bindings={
    (address, port): {
        'ztx': identity, 'service': service_name}
    })
def run_webapp(q_img, pipe_img_recv):
    """
    run the zitified webapp
    """
    web_config.modify_key("q_img", q_img)
    print(f"q_img in run_webapp: {q_img}")

    web_config.modify_key("pipe_img_recv", pipe_img_recv)
    print(f"pipe_img_recv in run_webapp: {pipe_img_recv}")

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, _signal_handler)
    loop.run_until_complete(
        serve(app, config, shutdown_trigger=shutdown_event.wait)
    )


def wrapper_run_webapp(q_img, pipe_img_recv):
    """
    Workaround for `AttributeError:
    Can't pickle local object 'zitify.<locals>.zitify_func.<locals>.zitified'`
    when process is started using forkserver method.
    """
    run_webapp(q_img, pipe_img_recv)


if __name__ == "__main__":

    run_webapp()

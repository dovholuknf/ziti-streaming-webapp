import openziti
# import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
import asyncio
from sse_starlette.sse import EventSourceResponse
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import time

from hypercorn.config import Config
from hypercorn.asyncio import serve
import signal

# for hypercorn
config = Config()
config.bind = ["localhost:8443"]
config.errorlog = "-" #stderr
config.loglevel = "DEBUG"
config.certfile = "local_cert_keep_secret.pem"
config.keyfile = "local_key_keep_secret.pem"

shutdown_event = asyncio.Event()

middleware = [
    Middleware(CORSMiddleware,
               allow_origins=["*"],
               allow_credentials=True,
               allow_methods=["*"],
               allow_headers=["*"],
               )
]

app = FastAPI(middleware=middleware)



templates = Jinja2Templates(directory="static")


@app.get("/")
async def indexpage(request: Request):
    return  templates.TemplateResponse(
        request=request, name="sse-client.html")


async def message_generator(request):
    for number in range(1, 256 + 1):
        if await request.is_disconnected():
            print("client disconnected!!!")
            break
        yield number
        time.sleep(1)


@app.get('/stream-sse')
async def message_stream(request: Request):
    event_generator = message_generator(request)
    return EventSourceResponse(event_generator)



def _signal_handler(*_: any) -> None:
    shutdown_event.set()


@openziti.zitify(bindings={
    ("localhost", 8443): {
        'ztx': "./predalert_server2.json", 'service': "predalert_service_2"}
    })
def run_webapp():
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, _signal_handler)
    loop.run_until_complete(
        serve(app, config, shutdown_trigger=shutdown_event.wait)
    )


if __name__ == "__main__":
    run_webapp()

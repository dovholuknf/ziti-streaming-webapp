import openziti
import uvicorn
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


middleware = [
    Middleware(CORSMiddleware,
               allow_origins=["*"],
               allow_credentials=True,
               allow_methods=["*"],
               allow_headers=["*"],
               )
]

app = FastAPI(middleware=middleware)

from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="static")


@app.get("/")
async def indexpage(request: Request):
    return  templates.TemplateResponse(
        request=request, name="sse-client.html")


async def slow_numbers(minimum, maximum):
    yield '<html><body><ul>'
    for number in range(minimum, maximum + 1):
        yield (b"--frame\r\nContent-Type:text/html\r\n\r\n" +
               b"<li>" + number.to_bytes() + b"</li>\r\n")

        await asyncio.sleep(0.5)
    yield '</ul></body></html>'

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



@openziti.zitify(bindings={
    ("127.0.0.1", 8443): {
        'ztx': "./predalert_server2.json", 'service': "predalert_service_2"}
    })
def run_webapp():
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=8443
        )


if __name__ == "__main__":
    run_webapp()

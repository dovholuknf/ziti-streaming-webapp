import openziti
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
import asyncio


app = FastAPI()


@app.get("/")
async def indexpage(request):
    return JSONResponse({"message": "Hello World"})


async def slow_numbers(minimum, maximum):
    yield '<html><body><ul>'
    for number in range(minimum, maximum + 1):
        yield (b"--frame\r\nContent-Type:text/html\r\n\r\n" +
               b"<li>" + number.to_bytes() + b"</li>\r\n")

        await asyncio.sleep(0.5)
    yield '</ul></body></html>'


@app.get("/stream")
async def stream_func():
    generator = slow_numbers(1, 256)

    return StreamingResponse(generator, media_type="multipart/x-mixed-replace; boundary=frame")


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

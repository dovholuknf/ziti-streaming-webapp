# Intro

Example of a zitified webapp, utilizing Hypercorn and Server-Sent Events for streaming of numbers and webcam.

# How to install
Python >=3.11

```
git clone https://gitlab.com/papiris/ziti-streaming-webapp.git
cd ziti-streaming-webapp
python -m venv .env
source .env/bin/activate
pip install .
```

# How to use

Change configurations in config.toml to suit your situation.

run `python -m ziti_streaming_webapp`

visit the ziti URL for number stream

visit `/video` sub-path for video stream


# Errors
### Queues created by `multiprocessing.Manager.Queue` don't work
When the app is zitified, mp.Manager.Queue queues don't have the same memory address across processes.

`frame_producer.py` gets a `queue.Queue` object, and `webapp.py` gets an AutoProxy[Queue] object:  
`q_img in frame_producer: <queue.Queue object at 0x7f74df1f1990>`  
`q_img in run_webapp: <AutoProxy[Queue] object, typeid 'Queue' at 0x7f50d2428410; '__str__()' failed>`.

In this small app, defining `q_img` in `__main__.py` as regular `multiprocessing.Queue` seems to work, but larger apps like [Predalert](https://gitlab.com/papiris/predator-detect-and-notify) fail with `OSError 32: Broken Pipe` for both mp.Manager.Queue and mp.Queue.  
Pipes work in smaller apps as well, but also struggle in Predalert.

### `11, 'Unexpected Error'` in zitilib.py

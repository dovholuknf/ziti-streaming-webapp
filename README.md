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
### AttributeErrors
```python
Process Process-3:
Traceback (most recent call last):
  File "/usr/lib64/python3.12/multiprocessing/process.py", line 314, in _bootstrap
    self.run()
  File "/usr/lib64/python3.12/multiprocessing/process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "/var/mnt/data/jacob/git/ziti_py_MWE/ziti_streaming_webapp/webapp.py", line 204, in wrapper_run_webapp
    run_webapp(q_img, ziti_dict)
  File "/var/mnt/data/jacob/git/ziti_py_MWE/ziti_streaming_webapp/webapp.py", line 191, in run_webapp
    loop = asyncio.get_event_loop()
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/asyncio/events.py", line 699, in get_event_loop
    self.set_event_loop(self.new_event_loop())
                        ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/asyncio/events.py", line 720, in new_event_loop
    return self._loop_factory()
           ^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/asyncio/unix_events.py", line 64, in __init__
    super().__init__(selector)
  File "/usr/lib64/python3.12/asyncio/selector_events.py", line 66, in __init__
    self._make_self_pipe()
  File "/usr/lib64/python3.12/asyncio/selector_events.py", line 120, in _make_self_pipe
    self._ssock, self._csock = socket.socketpair()
                               ^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.12/socket.py", line 610, in socketpair
    a = socket(family, type, proto, a.detach())
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/var/mnt/data/jacob/git/ziti_py_MWE/.env_3.12/lib64/python3.12/site-packages/openziti/decor.py", line 27, in __init__
    super().__init__(*args, **dict(kwargs, opts=patch_opts))
  File "/var/mnt/data/jacob/git/ziti_py_MWE/.env_3.12/lib64/python3.12/site-packages/openziti/zitisock.py", line 55, in __init__
    self._ziti_bindings = process_bindings(opts.get('bindings'))
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/var/mnt/data/jacob/git/ziti_py_MWE/.env_3.12/lib64/python3.12/site-packages/openziti/zitisock.py", line 28, in process_bindings
    for k in orig:
  File "<string>", line 2, in __iter__
  File "/usr/lib64/python3.12/multiprocessing/managers.py", line 827, in _callmethod
    proxytype = self._manager._registry[token.typeid][-1]
                ^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute '_registry'
Exception ignored in: <function BaseEventLoop.__del__ at 0x7f85a27dbe20>
Traceback (most recent call last):
  File "/usr/lib64/python3.12/asyncio/base_events.py", line 726, in __del__
    self.close()
  File "/usr/lib64/python3.12/asyncio/unix_events.py", line 68, in close
    super().close()
  File "/usr/lib64/python3.12/asyncio/selector_events.py", line 104, in close
    self._close_self_pipe()
  File "/usr/lib64/python3.12/asyncio/selector_events.py", line 111, in _close_self_pipe
    self._remove_reader(self._ssock.fileno())
                        ^^^^^^^^^^^
AttributeError: '_UnixSelectorEventLoop' object has no attribute '_ssock'
```

### `11, 'Unexpected Error'` in zitilib.py


### Error 107, transport endpoint not connected

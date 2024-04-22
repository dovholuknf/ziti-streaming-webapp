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
### `11, 'Unexpected Error'` in zitilib.py

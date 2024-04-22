# Intro

Example of a zitified webapp, utilizing Hypercorn and Server-Sent Events for streaming of numbers and webcam.

## How to install
Python >=3.11

```
git clone https://gitlab.com/papiris/ziti-streaming-webapp.git
cd ziti-streaming-webapp
python -m venv .env
source .env/bin/activate
pip install .
```

## How to use

Change configurations in config.toml to suit your situation. 

run `python -m ziti_streaming_webapp`

visit the ziti URL for number stream

visit `/video` sub-path for video stream

## Securing the app using OpenZiti

You can deploy and access your cameras anywhere without deploying firewalls
by configuring OpenZiti support. The config.toml file contains default values
for a server and a service that are expected to be used with OpenZiti. Change
as needed.

If you leave the defaults in place, you can test the solution with OpenZiti
by issuing the following ziti cli commands:

First get the latest version of the ziti CLI onto your path. This will be used
to create your developer environment and configure the overlay. This one line
command will use the `getZiti` function from `ziti-cli-functions.sh` to get the
latest version of `ziti`. The "yes" parameter instructs the fucntion to add `ziti`
to that shell session's path as well.
```
source /dev/stdin <<< "$(wget -qO- https://get.openziti.io/ziti-cli-functions.sh)"; getZiti yes
```

Once the `ziti` CLI exists, start a locally running ziti instance by using the 
provided quickstart:
```
ziti edge quickstart --home /tmp/persistence-dir
```

Now, start a new terminal window and put `ziti` back on your path. You can either
run the `getZiti` command (as shown before) or put `ziti` on your path however you want.
With `ziti` on the path you'll be able to configure your overlay network by running:
```
# use the default user/password to login to configure the overlay
ziti edge login -y -u admin -p admin

ziti edge create identity predalert_server2 -o ./predalert_server2.jwt
ziti edge enroll ./predalert_server2.jwt

ziti edge create identity predalert_client -o ./predalert_client.jwt
ziti edge create config predalert.int intercept.v1 '{"addresses":["predalert.ziti"],"portRanges":[{"high":80,"low":80}],"protocols":["udp","tcp"]}'
ziti edge create service predalert_service_2 --configs predalert.int 
ziti edge create service-policy predalert.bind Bind --service-roles @predalert_service_2 --identity-roles @predalert_server2
ziti edge create service-policy predalert.dial Dial --service-roles @predalert_service_2 --identity-roles @predalert_client
```

Now add the the predalert_client identity to your tunneler of choice and go to http://predalert.ziti/




## Errors
### `11, 'Unexpected Error'` in zitilib.py

# ZeroSeg API

REST API for [ZeroSeg Improved](https://github.com/samedamci/ZeroSeg) library. This API can be hosted on your Raspberry Pi device
for remote displaying information on LCD display purpose.

## Running

You probably don't need run it with extra options like HTTPS when you use it in your home
network. Of course if you want to deploy this API to be accesible outside your home you
always should enable TLS for example with NGINX reverse proxy + uWSGI or Gunicorn.

In this example you can see simplest way to run production server.

+ Install packages from PyPI.
```
$ pip3 install --user ZeroSeg_API gunicorn
```
+ Start server with Gunicorn CLI.
```
$ gunicorn ZeroSeg_API:app --log-file - --bind <LOCAL_IP>
```

# authmail: Email application for email 2FA and relaying messages through a buffer

Flexible email automation tool for web services and other applications. I wrote this for use of my portfolio website, [hicksm.dev](https://hicksm.dev), but left it flexible enough to be repurposed for most any application.

## Installation

This application was developed in Python 3.10, the only major requirement. Python packages required can be found in `src/authmail/requirements.txt`. You can simply run

```bash
pip install -r src/authmail/requirements.txt
```

and will be good to go with the base application.

## Quick Start

To get started, navigate to the `src/authmail/config` directory and make copies `%` from all files matching `%.template`. Look through all of these and make necessary adjustments. More info available below in the Usage section.

Once this application is configured and all necessary dependencies are installed, go back to `src/authmail` (one file up from current) and run `python uvicorn main:app`.

See the [REST API documentation](https://github.com/mwhicks-dev/authmail/wiki#api) for access info.

## Usage

This application is meant to be moreso developer-friendly than anything, as it is not that well fleshed out besides the stuff that I needed for my webserver when I made it. In `src/authmail/config/implementation` you can find some files providing examples for how to do things with the interfaces I have provided with or without the need for complex authorization workflows. That being said, you are welcome to reuse them, as all of the implementations in that directory depend only on other open-source software. 

I will walk through the configuration files in `src/authmail/config` in the order that you should set them up.

* Begin with `behavior.py`. This file is where you specify *what* behaviors (implementations of `src/authmail/behavior` interfaces) you would like to use for this application, all of which you can find (or reference while writing your own) in the `implementation/` subdirectory. If you don't select a ChallengeHandler and MailHandler, this application will not be able to run. However, any old MailHandler and ChallengeHandler should be interoperable.
* Next, modify `config.json`. You will likely need to implement the `app_name` field and all of the members of `smtp`, but technically, those (and all other) members of the config are dependant on the implementation you are using. If writing your own handler, add any passwords or keys here.
  * The `generate_docs` key determines whether a SwaggerUI implementation is generated using OpenAPI specification and available at `${host}:${port}/docs`. Usually, this should be false in deployed systems.
  * If you are planning to access authmail from a web service, you should set `origins` to an array of website you wish to be able to access it (for CORS purposes). 
* (Optional) Finally, modify `requirements.txt`. This is really only important so that Docker can build your application if you want it to.

With this out of the way, you should be able to navigate to `src/authmail` and run:

```bash
uvicorn main:app --host 0.0.0.0 --port {host-authmail-port}
```

to start the service. I would not recommend running with many workers unless the implementations you are using are specifically built for it. The basic infrastructure, however, is highly async compatible.

### Extension

Add a custom implementation to `src/authmail/config/implementation`. This is easy to reach and keeps everything user-defined in one place. For posterity sake, it is *highly recommended* that at the top of your implementation, you document any elements that need to be added to the `config.json` or `requirements.txt` files and other important details.

### Docker Usage

You can use the Dockerfile tob uild and run this service. Before building, you will need to verify or modify the following arguments:

* `TARGET`: This will be the branch (or tag) you would like to build to your Docker image (for instance `v1.0` or `dev`). If not modified, this argument defaults to `main`.
* `CONFIG_PATH`: Set this to the local path from your current directory when running `docker build` to the `config` directory. If not modified, this argument defaults to `src/authmail/config/`.

Build:

```bash
docker build --no-cache --build-arg TARGET={your-target-branch} -t authmail .
```

Use of `--no-cache` is recommended as authmail utilizes git. The Dockerfile will *temporarily* copy your `config/` directory in order to set up any dependencies, but this will be removed completely (`rm -rf`) before the image is finished building. You should rebuild whenever you:

1. Want to use a different version of authmail
1. Want to use a different set of behaviors with different dependencies (i.e. PyAcctMailHandler utilizes the Python `httpx` package)

Run:

```bash
docker run --rm \
    -v /$(pwd)/src/authmail/config/:/authmail/src/authmail/config/ \
    -p {host-authmail-port}:{container-port} \
    authmail --port {container-port} --workers {number-async-workers}
```

In the Docker image, a directory `cert` is available for you to provide your SSL info. To deploy with SSL enabled, instead run:

```bash
docker run --rm \
    -v /$(pwd)/src/authmail/config/:/authmail/src/authmail/config/ \
    -v /path/to/cert/readable/:/cert/ \
    -p {host-authmail-port}:{container-port} \
    authmail --port {container-port} --workers {number-async-workers} \
    --ssl-certfile /cert/cert.pem --ssl-keyfile /cert/privkey.pem --ssl-keyfile-password {your-kf-password}
```

You may need to copy your existing certs into a new container so that the Docker image has permission to read them. Make sure these are not accessible to the web!

You can detach with `-d`.

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

* Begin with `behavior.py`. This file is where you specify *what* behaviors (implementations of `src/authmail/behavior` interfaces) you would like to use for this application, all of which you can find (or reference while writing your own) in the `implementation/` subdirectory. If you don't select a ChallengeHandlker and MailHandler, this application will not be able to run. However, any old MailHandler and ChallengeHandler should be interoperable.
* Next, modify `config.json`. You will likely need to implement the `app_name` field and all of the members of `smtp`, but technically, those (and all other) members of the config are dependant on the implementation you are using. If writing your own handler, add any passwords or keys here.
* (Optional) Finally, modify `requirements.txt`. This is really only important so that Docker can build your application if you want it to.

With this out of the way, you should be able to navigate to `src/authmail` and run:

```bash
uvicorn main:app --host 0.0.0.0 --port {host-authmail-port}
```

to start the service. I would not recommend running with many workers unless the implementations you are using are specifically built for it. The basic infrastructure is highly async compatible.

### Extension

Add a custom implementation to `src/authmail/config/implementation`. This is easy to reach and keeps everything user-defined in one place.

### Docker Usage

You can use the Dockerfile tob uild and run this service. Before building, you will need to verify or modify the following argument:

* `TARGET`: This will be the branch (or tag) you would like to build to your Docker image (for instance `v1.0` or `dev`). If not modified, this argument defaults to `main`.

Build:

```bash
docker build --no-cache --build-arg TARGET={your-target-branch} .
```

Use of `--no-cache` is recommended as authmail utilizes git.

Run:

```bash
docker run --rm -it -v /$(pwd)/src/authmail/config/:/authmail/src/authmail/config/ -p {host-authmail-port}:8000 authmail
```

You can detach with `-d`.

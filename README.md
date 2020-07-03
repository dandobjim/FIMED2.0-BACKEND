## [FIMED-API]() 

---

<a href="https://github.com/benhid/drama"><img alt="Version: 0.0.1" src="https://img.shields.io/badge/version-0.0.1-success?color=0080FF&style=flat-square"></a>

Before running `fimed`, save a copy of [`.env.template`](.env.template) as `.env` and insert your own values. 

`fimed` will look for a valid `.env` file in the **current working directory**.
 In its absence, it will use environmental variables (environment variables will always take priority over values loaded from a dotenv file).

### 🚀 Setup 

#### Installation

Via source code:

```console
$ git clone git@github.com:dandobjim/FIMED2.0.git
$ cd FIMED2.0
$ python setup.py install
```

After that you can run:

```console
$ fimed -h
```

#### Deploy server 

Server can be [deployed](https://fastapi.tiangolo.com/deployment/) with *uvicorn*, a lightning-fast ASGI server, using the command-line client.

```console
$ fimed deploy
```

Online documentation is available at `/api/docs`.

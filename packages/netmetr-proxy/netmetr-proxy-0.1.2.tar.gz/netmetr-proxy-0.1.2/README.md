# ![NetMetr](https://www.netmetr.cz/theme/images/netmetr-logo.svg) `netmetr-proxy`

Helper proxy to sit between [netmetr](https://www.netmetr.cz/) web client and backend. Adds a token/key and calls backend for:

- Monthly stats approval
- Uncleaned data download

```
browser       netmetr-proxy          backend
   |                 |                   |
   |     GET         |     POST          |
   | --- month ----> | --- month-------> |
   |   + year        |   + year          |
   |                 |   + token         |
   |                 |                   |
   | <-- response -- | <-- response ---- |
   |   (zip or json) |                   |
   |                 |                   |
```

It also adds some input validation, since the backend will happily return empty CSVs for future dates or even a `.zip` file with plaintext `"illegal parameters"` content.

## Dependencies

- Python >= 3.6
- pyaml >= 17
- flask >= 0.12

## Installation

```
$ virtualenv -p `which python3.6` .venv
$ source .venv/bin/activate
$ pip install netmetr_proxy
$ cp config.example.yml config.yml
$ $EDITOR config.yml # set backend url & access token
```

### Running in production

uWSGI:

```
$ uwsgi --master --single-interpreter --threads 2 --http :5000 -H .venv -w netmetr_proxy.server
```

GUnicorn:

```
$ gunicorn -w 2 -k gevent --timeout 160 -n netmetr-proxy netmetr_proxy:server:app
```

## Usage

### Downloading uncleaned open data

```
GET /opendata
month <int>
year <int>
```

Returns opendata ZIP for download (`NetMetr-opendata-dirty-{year}-{month}.zip`).

### Monthly stats approval

```
GET /approve
month <int>
year <int>
```

Returns:

```
GET /approve?year=2018&month=3
-> 200
   {"success": true, "message": "Results for 2018-03 were successfully approved."}
```

if called again:

```
GET /approve?year=2018&month=3
-> 200
   {"success": true, "message": "Results for 2018-03 were already approved before."}
```

### Error responses

Returns errors from backend wrapped in JSON:

```
GET /opendata?year=2018&month=1
# invalid key in config results in "ERROR: invalid key!" message
# from backend (with HTTP 200 for some reason…)
-> 403
   {'error': 'invalid key!'}
```

Returns HTTP 400 and an error message for missing invalid params (bad format or future date):

```
GET /opendata?year=2018&month=0
-> 400
   {'error': 'Invalid date.'}
```

```
GET /opendata?year=0&month=march
-> 400
   {'error': 'Invalid date.'}
```

```
GET /approve?year=2018
-> 400
   {'error': 'Missing or invalid parameter (year, month).'}
```

Returns 404 for any non-existing endpoint:

```
GET /
-> 404
```

```
GET /foo
-> 404
```

## Development

Starting server with auto reload on file changes:

```
$ FLASK_APP=netmetr_proxy/server.py FLASK_DEBUG=1 flask run
```

Linting Python code:

```
$ flake8 --config=.flake8rc *py
```

## License

GPLv3

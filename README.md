# The wall
The wall project description

## Requirements
* docker-compose 19.0+
* python 3.10 (3.8+ will also works, but not sure)

# Run
## CLI tool
You can run both `singlethread` mode and `multithread` mode with CLI tool. Make sure you have installed `typer` or just run this commands:
* `pip install -r requirements.txt`
* `poetry install`

Run this to recieve help box:
```
poetry run python3 thewall/cli.py --help
```
(skip `poetry run` prefix if you don't use poetry environment)

Or just run either:
```
poetry run python3 thewall/cli.py singlethread
```
or
```
poetry run python3 thewall/cli.py multithread
```
`multithread` mode also accept `--teams=n` flag (default `5`).

For now this commands use `data/test.txt` as default input but you can change it as well as path to output logfile (`data/logs/log.singlethread.txt` and `data/logs/log.multithread.txt` by default).

Don't forget that help box is also available for both this commands:
```
poetry run python3 thewall/cli.py singlethread --help
```
or
```
poetry run python3 thewall/cli.py multithread --help
```

## WebApp
### With `docker-compose`
```
    docker-compose up
```
### Without `docker-compose`
* `pip install -r requirements.txt`
* `poetry install`
* Run postgresql and make sure you have corrensponding DB variables in `djangoapp.settings`
* `DJANGO_SETTINGS_MODULE=djangoapp.settings poetry run python3 -m django migrate`
* `DJANGO_SETTINGS_MODULE=djangoapp.settings poetry run python3 -m django runserver`

#### API setup
There are 2 steps to use **The Wall** api:
1. Set up input with POST:`/profiles/setup/multithread`
    This step run the same `TeamPool` class as `cli.py` in multithread mode, check `thewall.team_pool.TeamPool` for more details.
    Format:
    ```
    {
        "teams": 5, 
        "profiles": [[21, 25, 28], [17]],
        
        // OPTIONAL
        "team_power_per_day": 4, // default 1
        "team_sleep_per_foot": 0.5, // default 0.1
    }
    ```
    Example:
    ```
    curl -X "POST" localhost:8000/profiles/setup/multithread -H "Content-Type: application/json" -d '{"teams": 5, "profiles": [[21, 25, 28], [17], [17, 22, 17, 19, 17]]}' | json_pp
    ```
2. Use:`/profiles/*/cost` API to check cost and ice amount for different profiles and days.
    Example:
    ```
    curl -X "GET" localhost:8000/profiles/1/day/1/cost
    ```
3. *OPTIONAL* Reset setup with DELETE:`/profiles/setup/reset`

You can also check [Swagger API](http://localhost:8000/redoc/) to get more information about available methods.
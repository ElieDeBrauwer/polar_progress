# Polar progress

## Introduction

Polar progress is a little tool which queries the Polar Flow internal API (not the 
[Polar accesslink API](https://www.polar.com/accesslink-api/) which is not suitable for this purpose). It is partly inspired on 
[flow-client](https://github.com/campbellr/flow-client) but as the latter was also not really finished it does not depend on it 
directly.

The main goal is that you give it your Polar flow credentials and the number of kilometer you plan to run this year. It will then
query the progress you made to date and then report whether or not you're on track.

## Installation

Clone this repository, make sure the [requests](http://docs.python-requests.org/) library is availabe and you're good to go.

## Usage:

To make use of this polar progress you need a configuration file:
```javascript
{
    "login": "POLAR_USER",
    "password": "POLAR_PASS",
    "goal": 1000
}
```

And then you can invoke the tool as follows :
```
$./polar_progress.py -h
usage: polar_progress.py [-h] [--config CONFIG]

Polar Flow progress reporter

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  the configuration file (default: ./progress_settings.json)
$ ./polar_progress.py
Target: 1000 km
Daily target: 2.74 km/day
Expected distance to date: 38.4 km
Achieved distance: 81.8 km or 8.2%
You are 43.4 km or 15.8 days ahead of schedule
Extrapolated result: 2132.0 km at the end of the year
```


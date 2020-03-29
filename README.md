# Sports Stock Market Server

The server for the Sports Stock Market web application

## Installation

1. Download the git
2. Install the required packages:
    * Using pip, run `pip install -r requirements.txt`
    * Using Anaconda, run `conda create --name <env> --file environment.yml` where `<env>` is the name of your environment to create a new environment for this project (recommended) or run `conda env update --file environment.yml` to update (and rename!) your current environment.

## Running

In order to run this application, run the following commands in the `marketserver` folder (with the flask environment active if using Anaconda):
```bash
set FLASK_APP=fanbase.py
flask run
```

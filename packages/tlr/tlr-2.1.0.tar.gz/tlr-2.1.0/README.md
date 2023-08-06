# tlr

## Overview

`tlr` is a package that act as a service for VOGAMOS (Volcanic Gas Monitoring
System) data acquisition. It listens for data from telnet server, parse the
data, and store it to the database server.

## Deployment Guide

Clone the project from GitLab repository server:

    git clone https://gitlab.com/bpptkg/tlr.git

Then, change directory to the tlr root directory:

    cd tlr/

First, install Python virtual environment, pip, and MySQL library:

    sudo apt install python-virtualenv python3-pip python3-dev libmysqlclient-dev

Make Python virtual environment and activate the virtual environment:

    virtualenv -p python3 venv
    source venv/bin/activate

Install all package requirements:

    pip install -r requirements.txt

Then, copy project settings from `.env.example` file:

    cp .env.example .env

Set some important settings, including `DATABASE_ENGINE`, `TELNET_HOST`,
`TELNET_PORT`, `TELNET_TIMEOUT`, and `SENTRY_DSN`. Don't forget to set `DEBUG`
to `False` if used in the production environment.

If database table isn't migrated yet, you can run database migration by
executing this command:

    ./bin/migrate

Install Supervisord. We will use it to monitor script daemon process:

    sudo apt install supervisor

Copy Supervisord tlr configuration from `supervisor/` directory:

    sudo cp supervisor/tlr.conf /etc/supervisor/conf.d/

Edit `/etc/supervisor/conf.d/tlr.conf` according to your need:

    [program:tlr]
    directory=/path/to/tlr
    command=bash -c "source /path/to/tlr/venv/bin/activate && /path/to/tlr/run.py"
    autostart=true
    autorestart=true
    stdout_logfile=/var/log/supervisor/tlr.log
    stderr_logfile=/var/log/supervisor/tlr_error.log
    environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8

    [group:tlr]
    programs:tlr

In the configuration above, we start the service using the command:

    bash -c "source /path/to/tlr/venv/bin/activate && /path/to/tlr/run.py"

It will start the service within Python virtual environment and make sure that
we have only one process running.

Reread and update Supervisord configuration:

    sudo supervisorctl reread
    sudo supervisorctl update

You can view Supervisord status by running this command:

    sudo supervisorctl status

Finally, monitor your database if data has been stored.

## Monitoring for Errors

If any error occurred, you can see the error from the log file in
`storage/logs/tlr.log` (logging directory may be different if you use custom
`LOGGING_ROOT`), from Supervisord log (`/var/log/supervisor/tlr_error.log`), or
from [Sentry](https://sentry.io/organizations/bpptkg/issues/?project=5253584)
web interface.

Viewing error logs from Supervisord is basically good to debug system-related
errors. In addition to that, viewing from Sentry web is recommended to track
errors in the application level.

## Applying Code Updates

First, tap into deployment server via `ssh` or any other ways. Then, pull
updates from GitLab repository:

    cd /path/to/tlr/
    git pull

Restart tlr service:

    sudo supervisorctl restart tlr

If you ever modify tlr configuration in `/etc/supervisor/conf.d/tlr.conf`, you
have to reread and update the service:

    sudo supervisorctl reread
    sudo supervisorctl update

## Developer Reference

After cloning the project and creating Python virtual environment, install all
development package requirements:

    pip install -r dev-requirements.txt

Before submitting your changes to our GitLab repository, write unit test in the
`tests/` directory. You can run all unit tests to see if your test has passed by
running `pytest` command:

    pytest

Main script entry point is `run.py`. You can run the script by executing this
command:

    python run.py

Note that you have to run the script within your Python virtual environment.

## Installing tlr Library

If you want to access tlr API, you can install the package from PyPI:

    pip install -U tlr

Example:

```python
from tlr.parser import T1Parser
from tlr.utils import force_str

# Data from telner server
bytes_data = b'T#01 56.92,\r\nT#03 88.10,90.62,90.42,29.68,14.39\r\n \r\n C \xfc'

# Decode raw data to ordinary string format
str_data = force_str(bytes_data, errors='backslashreplace')

# Create a parser object
data_parser = T1Parser()

# Parse the data
cleaned_data = data_parser.parse_as_dict(str_data)

# Print cleaned data
print(cleaned_data)
```

Output:

    [{'temperature': 56.92}]

## Contributing

See `CONTRIBUTING.md` to learn how to contribute to this project.

## Support

This project is maintained by Indra Rudianto. If you have any question about
this project, you can contact him at <indrarudianto.official@gmail.com>.

## License

By contributing to the project, you agree that your contributions will be
licensed under its MIT license. See
[LICENSE](https://gitlab.com/bpptkg/tlr/-/blob/master/LICENSE) for details.

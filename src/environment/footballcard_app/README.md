# Ruby on Rails Tutorial sample application

This is the sample application for the
[*Ruby on Rails Tutorial:
Learn Web Development with Rails*](https://www.railstutorial.org/)
by [Michael Hartl](https://www.michaelhartl.com/).

## License

All source code in the [Ruby on Rails Tutorial](https://www.railstutorial.org/)
is available jointly under the MIT License and the Beerware License. See
[LICENSE.md](LICENSE.md) for details.

## Getting started

To get started with the app, clone the repo and then install the needed gems:

```
$ gem install bundler -v 2.3.14
$ bundle _2.3.14_ config set --local without 'production'
$ bundle _2.3.14_ install
```

Next, migrate the database:

```
$ rails db:migrate
```

Finally, run the test suite to verify that everything is working correctly:

```
$ rails test
```

If the test suite passes, you'll be ready to run the app in a local server:

```
$ rails server
```

For more information, see the
[*Ruby on Rails Tutorial* book](https://www.railstutorial.org/book).


## Setting up development PostgreSQL-16
Sources: https://www.cherryservers.com/blog/install-postgresql-ubuntu-22-04

To set up your development environment with PostgreSQL instal of sqlite, start with updating your system:

```
$ sudo  apt update
$ sudo apt upgrade -y
```

We will be using the official repository method.
Add the PostgreSQL repository:

```
$ sudo sh -c 'echo "deb https://apt.PostgreSQL.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
```

Import the repository signing key:

```
$ wget --quiet -O - https://www.PostgreSQL.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
```

Update your local package index:

```
$ sudo apt update
```

Install PostgreSQL v16:

```
$ sudo apt install postgresql-16 -y
```

Make sure to update the three lines to md5 in the file "/etc/postgresql/16/main/pg_hba.conf"

## PostgreSQL Commands
Use the following commands:

Start
```
$ sudo service postgresql start
or
$ sudo systemctl start postgresql
```

Check status
```
$ sudo systemctl status postgresql
```

Check background
```
$ sudo ss -pnltu | grep 5432
```

Restart
```
$ sudo systemctl restart postgresql
```

Reload
```
$ sudo systemctl reload postgresql
```

Stop
```
$ sudo systemctl stop postgresql
```

Access postgresql user prompt
```
$ sudo -i -u postgres psql
$ \q
$ exit
```

## Other
Watch the logs:
```
$ tail -f log/development.log
```

Log into the postgresql database:
```
$ sudo -i -u postgres
$ psql -U riley -d footballcard_app_development
```

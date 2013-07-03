django-get-evidence
===================

Welcome to Madeleine's Django rewrite of GET-Evidence, a work in progress. 
This is a project to recreate the functionality of the current GET-Evidence,
hosted at [evidence.personalgenomes.org](http://evidence.personalgenomes.org) with code available at
[github.com/PersonalGenomeProject/get-evidence](https://github.com/PersonalGenomeProject/get-evidence).

Installation
------------
These instructions were written for Ubuntu Linux (since that's what I use).
If you use another system, please go ahead and submit modifications to this file
to describe alternate instructions. Thanks!

### Clone the Git repository ###

* Navigate to the directory you want to have the code in, and clone the 
repository with: `git clone git://github.com/madprime/django-get-evidence`.

### Install Postgres and create database ###

1. **(Root user action)** Install Postgres with: `sudo apt-get install postgres` 
2. **(Postgres user action)** Create a new Postgres user with: `sudo -i -u postgres createuser getevidence -P`
with the password: `glassworks`. (This password a placeholder and is stored in the current settings,
developing a real password is a TODO.) You should answer "n" to superuser, "y" to creating databases,
and "n" to creating new roles.
3. **(Postgres user action)** Create a getevidence database with:
`sudo -i -u postgres createdb -O getevidence getevidence`

### Install required Python packages ###

* **(Root user action -- If you know virtualenv, please feel free to use that instead 
and update these instructions.)** Navigate to top directory in this project. (One of the subdirectories
should be "requirements".) Install the Python and Django packages required for development with 
`sudo pip install -r requirements/dev.txt`.

### Initialize database ###

1. Navigate to the django-get-evidence/getevidence/. Run `python manage.py syncdb`. You should probably 
create a superuser account for admin; set it to whatever you wish.

2. **(Optional)** Add sample data by running `python manage.py sample_data`.

### Run server ###

* You can now run a local version with `python manage.py runserver --settings=getevidence.settings.dev`

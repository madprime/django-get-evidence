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

### Install postgres, pip, virtualenv, and virtualenvwrapper ###

1. **(Root user action)** Install Postgres with: `sudo apt-get install postgresql` 
2. **(Root user action)** Install pip: `sudo apt-get install python-pip` 
3. **(Root user action)** Use pip to install virtualenv and virtualenvwrapper: `sudo pip install virtualenv virtualenvwrapper`.

### Set up virtualenv and virtualenvwrapper ###

1. Make a directory to store your virtual environments: `mkdir ~/.virtualenvs`
2. To make virtualenv and virtualenvwrapper commands work in future terminals, add the 
following to your bashrc (or zshrc, as appropriate): 
`export WORKON_HOME=$HOME/.virtualenvs` and
`source /usr/local/bin/virtualenvwrapper.sh`.

### Make a virtual environment and install required Python packages ###

If you open a new terminal you should now be able to access the virtualenvwrapper commands listed below.

If you aren't familiar with pip and virtualenv: these are standard aspects of Python development,
greatly facilitating package management. Whenever working on this software you should do so within
the virtual environment (e.g. after performing step 2 below).

1. Create a new virtual environment for working on this code: `mkvirtualenv getevidence`
2. Start using this virtual environment: `workon getevidence`
3. Navigate to top directory in this project. (One of the subdirectories
should be "requirements".) Install the Python packages required for development with 
`pip install -r requirements/dev.txt`.

### Create and initialize database ###

1. **(Postgres user action)** Create a new Postgres user with: `sudo -i -u postgres createuser getevidence -P`
with the password: `glassworks`. (This password a placeholder and is stored in the current settings,
developing a real password is a TODO.) You should answer "n" to superuser, "y" to creating databases,
and "n" to creating new roles.
2. **(Postgres user action)** Create a getevidence database with:
`sudo -i -u postgres createdb -O getevidence getevidence`
3. Navigate to the django-get-evidence/getevidence/. Run `python manage.py syncdb`. You should probably 
create a superuser account for admin; set it to whatever you wish.
4. Add gene data by running: `python manage.py add_external_gene_data ../external_data/getevidence_external_gene_data.csv`
5. **(Optional)** Add sample data by running `python manage.py sample_data`.

### Run server ###

* You can now run a local version with `python manage.py runserver`

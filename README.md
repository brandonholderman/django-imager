# Imager

**Author**: Tyler Fishbone and Brandon Holderman
**Version**: 0.0.3

## Overview
This website will be an imgur analog, made to for use in learning how to use the Django web framework.

## Getting Started
Eventually this will simply be a URL that you can go to to use the website.
For developer use:
1. clone this repo
2. create a database in postgres called `imager`
3. create an ENV, once inside the ENV run `pip install -r requirements.txt`. You must be in the directory with the requirements.txt for this to work.
4. start the server by running `./manage.py runserver`
5. visit your localhost port 8000 to interact with the site
6. to create a superuser run `./manage.py createsuperuser` and add in your credentials.

## Architecture
This application utilizes the Django web framework and postgresql for its databse

## Change Log
* 2018-04-26 = 2300 - created profile page, random home image, library and photo viewing pages
* 2018-04-25 - 1700 - created album and photo models and extended testing.
* 2018-04-24 - 1700 - created user models and initial css changes.
* 2018-04-23 - 1700 - initial scaffold complete.

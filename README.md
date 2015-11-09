Developed on Ubuntu
Requires pymol, sqlite3
(sudo apt-get install pymol)
(sudo apt-get install sqlite3)

Credits for file upload form (and general file structure) go to:

minimal-django-file-upload-example (https://github.com/axelpale/minimal-django-file-upload-example.git)

Usage (Django 1.8)
------------------
First ensure you have Django 1.8 installed. Then:

    $ git clone https://github.com/michalstepniewski/TMProteins4.git
	$ cd myproject
	$ python manage.py migrate
	$ python manage.py runserver


Note: *Module.py files contain old modules that I wrote for a different (wider) purpose when I saw myself more as a scientist that happened to write scripts for own use rather than developer and show some unoptimalized features as well as functions that are currently not used but probably will be as the app develops. I keep them in unchanged form as the main purpose of this app is 'proof of concept' of using django to visualize and as GUI for my previous work.

# TMProteins

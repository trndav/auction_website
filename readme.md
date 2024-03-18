## Commerce project 

First to properly create auctions_user:

python manage.py makemigrations auctions
python manage.py migrate

* To seed some categories, users, listings and comments:
* python manage.py seed_categories
* python manage.py seed_users_items
* python manage.py runserver

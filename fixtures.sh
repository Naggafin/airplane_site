#!/bin/sh

python3 manage.py loaddata sandbox/fixtures/child_products.json
python3 manage.py oscar_import_catalogue sandbox/fixtures/*.csv
python3 manage.py oscar_import_catalogue_images sandbox/fixtures/images.tar.gz
python3 manage.py oscar_populate_countries --initial-only
python3 manage.py loaddata sandbox/fixtures/pages.json sandbox/fixtures/ranges.json sandbox/fixtures/offers.json
python3 manage.py loaddata sandbox/fixtures/orders.json
python3 manage.py clear_index --noinput
python3 manage.py update_index catalogue
python3 manage.py thumbnail cleanup
python3 manage.py collectstatic --noinput

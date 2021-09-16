Requires postgresql with UTF-8 encoding and python 3(.9) 
```
pip install -r requirements.txt
cd solutional
python manage.py migrate
python manage.py loaddata product.json
python manage.py runserver PORT_NUMBER
```
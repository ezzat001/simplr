@echo off
echo Starting application...
call ..\Scripts\activate
python manage.py runserver 0.0.0.0:8000
pause
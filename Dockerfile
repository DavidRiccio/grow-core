FROM python:3.11

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["bash", "-c", "python manage.py runserver 0.0.0.0:8000 & python manage.py run_bot"]

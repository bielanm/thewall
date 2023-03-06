FROM python:3.10.9

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app

WORKDIR /app
RUN poetry install
EXPOSE 8000

CMD ["poetry", "run", "python3", "-m", "django", "runserver", "0.0.0.0:8000"]
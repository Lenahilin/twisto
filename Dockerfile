FROM python:latest
COPY . /twisto-test-task
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

EXPOSE 5000

CMD ["python", "/twisto-test-task/main.py"]
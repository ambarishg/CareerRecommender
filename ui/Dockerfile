FROM python:3.8-slim-buster
COPY . /app
WORKDIR /app
RUN pip install  -r requirements.txt --no-cache-dir
EXPOSE 5000

CMD ["python", "app.py"]
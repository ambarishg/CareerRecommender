FROM python:3.8-slim-buster
COPY . /app
WORKDIR /app
RUN pip install  -r requirements.txt --no-cache-dir
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
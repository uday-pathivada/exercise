# Dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install flask kubernetes
EXPOSE 5000
CMD ["python", "api.py"]


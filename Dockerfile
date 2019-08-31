FROM python:3.6.8-alpine
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . /app
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["app.py"]
FROM python:3.10-slim

WORKDIR /code

COPY . .

RUN pip install -r /code/requirements.txt

EXPOSE 1488

CMD ["python", "/code/web_app.py"]

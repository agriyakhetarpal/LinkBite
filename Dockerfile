FROM python:3.9

WORKDIR /app

RUN chown -R 1000:1000 /app

RUN chmod -R u+rwx /app

COPY . .

RUN pip install --no-cache-dir --upgrade  -r requirements.txt

RUN chmod +x run.sh

CMD ./run.sh
FROM python:3.9

WORKDIR /app

RUN chown -R 1000:1000 /app

RUN chmod -R u+rwx /app

COPY . .

RUN pip install --no-cache-dir --upgrade  -r requirements.txt

CMD ["uvicorn", "shortener.main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD ["python", "gradio-app.py"]
FROM python:3.12

RUN apt-get update && apt-get install python3-pip -y && pip install --upgrade pip && pip install pipenv

RUN mkdir -p /codebot
WORKDIR /codebot
COPY requirements.txt requirements.txt
COPY bot.py bot.py
EXPOSE 5000

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
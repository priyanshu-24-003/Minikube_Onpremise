FROM python:3.11-slim

#Creating a workdir named app The entire docker image is built on this Folder
WORKDIR /app

#Copying flask_app dir to the app dir
COPY app_mic2/ /app/app_mic2/

COPY pyproject.toml /app/
COPY setup.py /app/
COPY requirements.txt /app/

#moving src_utils
COPY src_utils/ /app/src_utils/

COPY data/bin /app/data/bin

ENV PYTHONUNBUFFERED=1

#exporting the dependencies in the docker image for our docker container to use.
#This requirements.txt is actually from inside the app.
RUN pip install -r requirements.txt

RUN pip list

EXPOSE 5000

#local
CMD ["python", "-u", "app_mic2/app.py"]  

#Prod
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]
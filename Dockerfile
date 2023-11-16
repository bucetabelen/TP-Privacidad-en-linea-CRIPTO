FROM python:3.10

COPY ./ad_server /root/ad_server
WORKDIR /root/ad_server
#RUN pip install -r requirements.txt
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

ENTRYPOINT ["pipenv", "run", "start_docker"]

#ENTRYPOINT ["python", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]

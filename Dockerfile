FROM python:3.9

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src /src
ENV FLASK_APP=/src/reservations_chambres

CMD [ "flask", "run", "--host=0.0.0.0", "--debug" ]

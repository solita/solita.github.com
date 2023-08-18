FROM python:3.11-alpine

WORKDIR /usr/src/app
RUN apk update && apk add git

RUN adduser -D rulekeeper
USER rulekeeper

COPY requirements.txt .
RUN ls
RUN pip install --no-cache-dir -r requirements.txt
RUN git config --global --add safe.directory /usr/src/app

CMD [ "python", "./rule-keeper/main.py" ]

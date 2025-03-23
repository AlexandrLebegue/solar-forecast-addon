FROM python:3.11

COPY run.sh /
COPY app.py /
COPY requirements.txt /



RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod a+x /run.sh
RUN ls -l /run.sh




CMD ["sh", "run.sh"] 

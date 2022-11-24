FROM python:3.11-alpine
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ADD scale.py /scale.py
ENTRYPOINT ["python", "-u", "/scale.py"]

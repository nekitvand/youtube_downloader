FROM python:3.10
WORKDIR code
COPY src .
RUN python3 -m pip install --upgrade pip && pip3 install -r requirements.txt
ENV FLAG $FLAG
ENV VALUE $VALUE
CMD ["sh", "-c","python download.py ${FLAG} ${VALUE}"]
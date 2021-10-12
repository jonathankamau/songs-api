FROM python:3.9

LABEL application="Songs API"

ENV PYTHONUNBUFFERED 1
RUN mkdir /api
WORKDIR /api
COPY . /api
RUN pip install -r requirements.txt
COPY scripts/dev.sh /dev.sh
RUN sed -i 's/\r//' /dev.sh \
    && chmod +x /dev.sh

ENTRYPOINT [ "/dev.sh" ]
FROM python:3.9

LABEL application="Songs API"

ENV PYTHONUNBUFFERED 1
RUN mkdir /api
WORKDIR /api
COPY . /api/
RUN pip install -r requirements.txt
COPY scripts/test.sh /test.sh
RUN sed -i 's/\r//' /test.sh \
    && chmod +x /test.sh

ENTRYPOINT [ "/test.sh" ]
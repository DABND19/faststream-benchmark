FROM python:3.11-bullseye

RUN mkdir /app
WORKDIR /app

RUN python3 -m venv venv

COPY requirements.txt .
RUN venv/bin/pip3 install -r requirements.txt

COPY faststream_bench faststream_bench
COPY dist dist

ARG faststream_package=faststream
RUN venv/bin/pip3 install ${faststream_package}

CMD ["venv/bin/python3", "-m", "faststream_bench.consumer"]

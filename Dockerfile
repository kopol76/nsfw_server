FROM debian:buster-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    caffe-cpu \
    python3 \
    python3-dev \
    python3-numpy \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    ffmpeg \
    libmagic-dev \
    file \
    && pip3 install numpy requests pillow \
    && rm -rf /var/lib/apt/lists/*

ADD . /workspace/
WORKDIR /workspace



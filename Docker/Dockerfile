FROM ubuntu:bionic
ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get update && apt-get install -y \
    openjdk-8-jre \
	python3 \
	python3-pip \
	wget \
	unzip

WORKDIR /
# Link to download TreeCmp
RUN wget https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3422086/bin/EBO-8-2012-475-s001.zip
RUN unzip EBO-8-2012-475-s001.zip

RUN pip3 install pandas dendropy scipy

COPY score.py /usr/local/bin/score.py
COPY score_sc1.py /usr/local/bin/score_sc1.py
COPY score_sc3.py /usr/local/bin/score_sc1.py
COPY validate_sc1.py /usr/local/bin/validate_sc1.py
COPY validate.py /usr/local/bin/validate.py
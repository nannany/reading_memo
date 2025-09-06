FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update
RUN apt-get -y install python3 python3-pip wget

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get -y install ./google-chrome-stable_current_amd64.deb

RUN pip3 install -r ./requirements.txt --break-system-packages

RUN echo ictf{testing_flag_1} > /flag.txt
ENV FLAG_2 ictf{testing_flag_2}

CMD ["flask", "run", "-h", "0.0.0.0"]

FROM python:3.12 
RUN mkdir /usr/src/pr-delta-comment-app
WORKDIR /usr/src/pr-delta-comment-app
COPY . .
RUN chmod +x bin/snyk-pr-delta-comment
RUN apt-get update --fix-missing
RUN apt-get -y install curl
RUN pip install -r ./requirements.txt
RUN curl --compressed https://static.snyk.io/cli/latest/snyk-linux -o snyk
RUN chmod +x ./snyk
RUN mv snyk bin
ADD https://github.com/snyk-tech-services/snyk-delta/releases/download/v1.12.0/snyk-delta-linux .
RUN chmod +x ./snyk-delta-linux
RUN mv snyk-delta-linux bin/snyk-delta
ENV PATH="/usr/src/pr-delta-comment-app/bin:$PATH"
EXPOSE 3000
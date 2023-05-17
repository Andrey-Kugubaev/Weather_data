FROM python:3.10-slim

WORKDIR /app
COPY . /app
COPY entrypoint /bin
WORKDIR /bin
RUN chmod +x entrypoint
WORKDIR /app
ENTRYPOINT entrypoint

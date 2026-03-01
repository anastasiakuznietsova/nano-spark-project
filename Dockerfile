FROM eclipse-temurin:17-jdk-jammy

WORKDIR /app

# Python 3 + pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/python3 /usr/bin/python

# PySpark
RUN pip3 install --no-cache-dir pyspark

COPY . /app

# run
CMD ["python", "main.py"]
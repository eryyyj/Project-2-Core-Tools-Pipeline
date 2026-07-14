# will use a slim version of Python 3.12 
FROM python:3.12-slim

# will install Java and other dependencies needed for PySpark
RUN apt-get update && \
    apt-get install -y default-jre curl bash && \
    apt-get clean;

# install git for the dbt project
RUN apt-get update && apt-get install -y git 

# set up the JAVA_HOME environment variable for PySpark
ENV JAVA_HOME=/usr/lib/jvm/default-java

# setting the working directory to /app
WORKDIR /app

# will copy the requirements.txt file into the container and install the dependencies
COPY requirements.txt .
ENV TMPDIR=/app
RUN pip install --no-cache-dir -r requirements.txt

# will copy the directory contents into the container
COPY . .

# this part keeps the container running so that you can exec into it and run commands interactively
CMD ["tail", "-f", "/dev/null"]
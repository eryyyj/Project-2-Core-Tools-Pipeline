# 1. Start with a lightweight Python 3.12 base image
FROM python:3.12-slim

# 2. Install system-level dependencies (Java for PySpark, curl for your shell script)
RUN apt-get update && \
    apt-get install -y default-jre curl bash && \
    apt-get clean;

# 3. Set Java Environment Variable so PySpark can find it
ENV JAVA_HOME=/usr/lib/jvm/default-java

# 4. Set up the working directory inside the container
WORKDIR /app

# 5. Copy your requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your repository into the container
COPY . .

# 7. Keep the container running indefinitely so you can run scripts manually
CMD ["tail", "-f", "/dev/null"]
FROM python:3.12.1-alpine
WORKDIR /app/
COPY requirements.txt .
COPY . /app/
RUN chmod +x start.sh
RUN pip install --no-cache-dir -r requirements.txt

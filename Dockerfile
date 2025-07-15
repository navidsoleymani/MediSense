# 🐍 Base Image: Lightweight Python 3.12
FROM python:3.12-slim

# Ensures Python output is sent straight to terminal (no buffering)
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /app

# 🔧 Install useful debugging tools: ping, curl, dig/nslookup
# These are helpful during container network diagnostics
RUN apt-get update && apt-get install -y \
    iputils-ping \
    curl \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# 📦 Copy and install project dependencies from requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 📂 Copy entire Django project source code into the container
COPY . /app/

# 🌐 Expose default Django port (Gunicorn listens on 8000)
EXPOSE 8000

# 🚀 Production entrypoint: Run Gunicorn WSGI server with gevent workers
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120", "--worker-class", "gevent"]

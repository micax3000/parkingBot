FROM python:3-slim
WORKDIR /app
COPY . .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 80
CMD ["python3", "main.py"]
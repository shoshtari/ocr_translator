FROM python:3.12-slim 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN apt update -o Acquire::Check-Valid-Until=false
RUN apt install tesseract-ocr -y

RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt /src/
RUN pip install -r requirements.txt 

COPY . /src/

# Expose the port that the app runs on
EXPOSE 4040

# Command to run the application using Gunicorn
CMD ["python", "/src/main.py"]

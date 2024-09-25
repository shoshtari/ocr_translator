FROM python:3.12-slim 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN apt update -o Acquire::Check-Valid-Until=false
RUN apt install -y tesseract-ocr ffmpeg libsm6 libxext6  

RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt /src/
RUN pip install -r requirements.txt 

COPY . /src/

# Expose the port that the app runs on
EXPOSE 4040

CMD ["python", "/src/main.py"]

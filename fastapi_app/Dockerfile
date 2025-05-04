FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxrender1 libxext6 \
    ffmpeg libgl1-mesa-glx build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY ./id_document_ocr /id_document_ocr

WORKDIR /id_document_ocr

EXPOSE 8001

RUN pip install --upgrade pip && \
    pip install -r /id_document_ocr/requirements.txt && \
    adduser --disabled-password --no-create-home duser && \
    chown -R duser:duser /id_document_ocr

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
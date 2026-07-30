FROM python:3.11-slim

ARG WORKDIR=/app

WORKDIR $WORKDIR

COPY ./src ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8100

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8100","--reload"]
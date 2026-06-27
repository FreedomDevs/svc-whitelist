FROM python:3.14-alpine

RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
  apk add --no-cache git && pip install --no-cache-dir -r requirements.txt && apk del git && rm -rf /root/.cache

COPY app/ app/
RUN python -m compileall -q /app

ENV PYTHONDONTWRITEBYTECODE=1
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "::", "--port", "80"]

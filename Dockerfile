FROM python:3.14-alpine

RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
  pip install --no-cache-dir -r requirements.txt

COPY app/ app/

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "::", "--port", "80"]

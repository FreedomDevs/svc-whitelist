FROM elysium-registry.mcbeeland.ru/svclibs:latest

#RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
#    grep -v "svcLibs" requirements.txt | pip install --no-cache-dir -r /dev/stdin && rm -rf /root/.cache

COPY app/ app/
RUN python -m compileall -q /app

ENV PYTHONDONTWRITEBYTECODE=1
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "::", "--port", "80"]

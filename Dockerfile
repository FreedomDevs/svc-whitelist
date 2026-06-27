FROM python:3.14-alpine

ARG SVCLIBS_COMMIT=unknown
RUN apk add --no-cache git && \
    if [ "${SVCLIBS_COMMIT}" = "unknown" ] || [ -z "${SVCLIBS_COMMIT}" ]; then \
        pip install --no-cache-dir git+https://github.com/FreedomDevs/svcLibs.git; \
    else \
        pip install --no-cache-dir git+https://github.com/FreedomDevs/svcLibs.git@${SVCLIBS_COMMIT}; \
    fi && \
    apk del git && rm -rf /root/.cache
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    grep -v "svcLibs" requirements.txt | pip install --no-cache-dir -r /dev/stdin && rm -rf /root/.cache

COPY app/ app/
RUN python -m compileall -q /app

ENV PYTHONDONTWRITEBYTECODE=1
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "::", "--port", "80"]

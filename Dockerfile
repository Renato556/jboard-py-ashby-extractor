# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /src

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN chown -R appuser:appuser /src
ENV HOME=/src

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container (já com o dono correto).
COPY --chown=appuser:appuser . .

# Create a script to run the job immediately on startup and then every 6 hours
RUN echo '#!/bin/bash\necho "Starting initial job extraction at $(date)"\npython -m src.main\necho "Initial job completed at $(date)"\nwhile true; do\n  echo "Sleeping for 6 hours..."\n  sleep 21600\n  echo "Starting scheduled job extraction at $(date)"\n  python -m src.main\n  echo "Scheduled job completed at $(date)"\ndone' > /src/run_periodic.sh && chmod +x /src/run_periodic.sh

# Run the periodic job
CMD ["/bin/bash", "/src/run_periodic.sh"]

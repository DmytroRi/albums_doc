# Dockerfile for build for backend
FROM <CENSORED_BASE_IMAGE>:latest-onUbuntu.24.04 AS base

# Set environment variables
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /workspace

# Copy source code
COPY .python-version .
COPY pyproject.toml .

# Development stage
FROM base AS development
ARG USER_STAGE="vscode"

# Rename existing ubuntu user to ${USER_STAGE} and ensure proper setup
RUN usermod -l ${USER_STAGE} -d /home/${USER_STAGE} -m ubuntu \
    && groupmod -n ${USER_STAGE} ubuntu \
    && echo "${USER_STAGE} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

ENV PYENV_ROOT_USER="/home/${USER_STAGE}/.pyenv"
RUN mkdir -p $PYENV_ROOT_USER && \
    cp -r ${PYENV_ROOT}/* $PYENV_ROOT_USER/ && \
    chown -R ${USER_STAGE}:${USER_STAGE} $PYENV_ROOT_USER

RUN chown -R ${USER_STAGE}:${USER_STAGE} /workspace

# Switch to vscode user for development
USER ${USER_STAGE}

# Set a user specific pyenv root
ENV PYENV_ROOT=${PYENV_ROOT_USER}
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:/home/${USER_STAGE}/.local/bin:$PATH"

# Initialize and rehash
RUN eval "$(pyenv init --path)" && \
    eval "$(pyenv init -)" && \
    pyenv rehash && \
    python -m venv .venv

ENV PATH="/workspace/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Command for development
CMD ["uvicorn", "incident_service.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# Test stage
FROM development AS test

# Set environment variables for maximum logging output
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTEST_ADDOPTS="--log-cli-format='%(asctime)s [%(levelname)8s] %(name)s: %(message)s'" \
    TOX_PARALLEL_NO_SPINNER=1

# Copy source code
COPY . .
USER root
RUN chown -R ${USER_STAGE}:${USER_STAGE} .
USER ${USER_STAGE}

# Debug: Verify tests directory exists and list contents
RUN ls -la /workspace/tests/ || echo "tests/ directory not found"

# Install dev dependencies (including tox) using pyenv's Python
RUN eval "$(pyenv init --path)" && \
    eval "$(pyenv init -)" && \
    . .venv/bin/activate && \
    python -m pip install -e .[dev]

# Run migrations + migration check before starting the app
RUN chmod +x /workspace/entrypoint.sh /workspace/migrate.sh
ENTRYPOINT ["/workspace/entrypoint.sh", "--check"]
CMD ["uvicorn", "incident_service.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# Production stage
# All files and dependencies are created or installed using the root user
# Right after the container switches to appuser for safer execution.
FROM base AS production
ARG USER_STAGE="appuser"

# Create non-root user
RUN groupadd -r ${USER_STAGE} && useradd -r -g ${USER_STAGE} ${USER_STAGE}

# Copy the actual source code into the image
COPY . .
RUN chown -R ${USER_STAGE}:${USER_STAGE} /workspace

# Make sure pyenv's shims are first in PATH
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"

# Install production dependencies and package (non-editable)
# this shall be done with root user such that USER_STAGE user
# cannot modify the python environment
RUN pip install --upgrade pip setuptools~=68 wheel && \
    pip install .

# Make entrypoint executable
RUN chmod +x /workspace/entrypoint.sh /workspace/migrate.sh

# Switch to non-root user
USER ${USER_STAGE}

# Expose port
EXPOSE 8000

ENTRYPOINT ["/workspace/entrypoint.sh"]
CMD ["python", "-m", "uvicorn", "incident_service.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

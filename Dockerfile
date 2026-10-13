# Reproducible environment for the verification scripts (SageMath from conda-forge).
# NOTE: this file was written but not test-built by the authors; the scripts were run in the same
#       conda-forge environment (environment.yml) installed directly with micromamba.
#
#   docker build -t rank112 .
#   docker run --rm rank112 python verify/01_basic.py
#   docker run --rm rank112 python verify/theta_series.py --table
FROM mambaorg/micromamba:1.5.10
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
RUN micromamba install -y -n base -f /tmp/environment.yml && micromamba clean --all --yes
ARG MAMBA_DOCKERFILE_ACTIVATE=1
WORKDIR /work
COPY --chown=$MAMBA_USER:$MAMBA_USER . /work
CMD ["python", "verify/01_basic.py"]

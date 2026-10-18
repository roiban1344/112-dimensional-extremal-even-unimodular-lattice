# SageMath image for the supplementary and data-producing computations: code/supplementary/,
# code/produce/, code/crosscheck/all_data/ and code/run_supplementary.sh. It is NOT needed for
# the proof (levels (i)-(iii) use the light image, Dockerfile). The build downloads 2-3 GB.
#
#   docker build -f Dockerfile.sage -t l112-sage .
#   docker run --rm l112-sage python3 -I code/supplementary/genus/genus.py check
#   docker run --rm l112-sage sage -c 'print(version())'
#   docker run --rm -v "$PWD/out:/work/out" l112-sage bash code/run_supplementary.sh
FROM mambaorg/micromamba:2.3.2

USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libc6-dev curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*
USER $MAMBA_USER

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
RUN micromamba install -y -n base -f /tmp/environment.yml && micromamba clean -a -y

# The micromamba entrypoint activates the base environment for CMD and docker run.
ARG MAMBA_DOCKERFILE_ACTIVATE=1
WORKDIR /work
COPY --chown=$MAMBA_USER:$MAMBA_USER . /work

CMD ["python3", "code/verify/v0_inputs.py"]

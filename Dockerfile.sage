# SageMath image for the supplementary and data-producing computations: code/supplementary/,
# code/produce/, code/crosscheck/all_data/ and code/run_supplementary.sh. It is NOT needed for
# the proof (levels (i)-(iii) use the light image, Dockerfile). The build downloads 2-3 GB.
#
#   docker build -f Dockerfile.sage -t l112-sage .
#   docker run --rm l112-sage python3 -I code/supplementary/genus/genus.py check
#   docker run --rm l112-sage sage -c 'print(version())'
#
# The supplementary computations read the verification data (.npz files, not in the image: they are
# downloaded by fetch.sh) and, for gluing_b, the output of verify/v4. Mount certificates/ and out/ of
# a clone of this repository, as for the light image, so that the download and the results stay on
# the host. Create out/ first (Docker would otherwise create it owned by root), and run as your own
# user: the user of the base image (mambauser, uid 57439) cannot write to a directory owned by you.
# All 30 steps take about 6 hours on one core (code/run_supplementary.sh, header); name steps to run
# only some of them, e.g. `bash code/run_supplementary.sh genus_check frames`.
#   mkdir -p out
#   docker run --rm --user "$(id -u):$(id -g)" -v "$PWD/certificates:/work/certificates" -v "$PWD/out:/work/out" \
#       l112-sage bash -c 'bash code/verify/fetch.sh && python3 -I code/verify/v4_norm8_orbits.py && bash code/run_supplementary.sh'
# The base image is pinned by digest (mambaorg/micromamba:2.3.2); environment.yml fixes the versions of SageMath,
# Python and numpy. / 基底イメージはダイジェストで固定する。environment.yml は SageMath・Python・numpy の版を固定する。
FROM mambaorg/micromamba:2.10.0@sha256:e1476182cd40eb1f7c0cfae4adec9bfd78f3d7f05c61368306abfdc8939c1198

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

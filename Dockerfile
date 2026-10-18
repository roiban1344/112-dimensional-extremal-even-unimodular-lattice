# Light image for the numpy-only verification (levels (i), (ii), (iii) of the README).
# No SageMath, no Lean: those are not needed for the proof. See Dockerfile.sage for the
# supplementary computations.
#
#   docker build -t l112 .
#
# (i) Inputs only (about 20 s); this is the default command:
#   docker run --rm l112
#
# (ii) The computational part of the proof (about 1.2 CPU hours). Mount the host directories
#      certificates/ and out/ of a clone of this repository, so that the 130 MB download and the
#      results survive the container (the host user should have uid 1000, as the user in the image):
#   mkdir -p out
#   docker run --rm -v "$PWD/certificates:/work/certificates" -v "$PWD/out:/work/out" l112 \
#       bash -c 'bash code/verify/fetch.sh && bash code/verify/proof.sh'
#
# (iii) Everything (about 26 CPU hours with three workers):
#   docker run --rm -v "$PWD/certificates:/work/certificates" -v "$PWD/out:/work/out" l112 \
#       bash -c 'bash code/verify/fetch.sh && bash code/verify/full.sh 3'
#
# The genus certificates (numpy only, about 90 s):
#   docker run --rm l112 python3 -I code/supplementary/genus/genus.py check
FROM debian:trixie-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      python3 python3-venv python3-pip gcc libc6-dev curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --uid 1000 --shell /bin/bash lattice \
 && mkdir /work && chown lattice:lattice /work
USER lattice
WORKDIR /work

# The venv is created first so that the layer with numpy is cached when only the sources change.
ENV VIRTUAL_ENV=/work/.venv
ENV PATH="/work/.venv/bin:${PATH}"
COPY --chown=lattice:lattice requirements-verify.txt /work/
RUN python3 -m venv "$VIRTUAL_ENV" \
 && python3 -m pip install --no-cache-dir -r requirements-verify.txt

COPY --chown=lattice:lattice . /work

CMD ["python3", "code/verify/v0_inputs.py"]

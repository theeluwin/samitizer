# from
FROM python:3.7-slim
LABEL maintainer="Jamie Seol <jamie@europa.snu.ac.kr>"

# uchardet
RUN apt-get update \
    && apt-get install -y --no-install-recommends uchardet \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

# init
RUN mkdir -p /workspace
WORKDIR /workspace

# test env
RUN pip install setuptools nose nose-exclude flake8 coverage coveralls

# run
ADD . /workspace/
RUN python setup.py build && \
	python setup.py install
ENTRYPOINT []
CMD ["nosetests", "--config=.noserc"]

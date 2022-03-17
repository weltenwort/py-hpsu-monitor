FROM python:3.10.3-alpine as base

RUN adduser --disabled-password py-hpsu-monitor
USER py-hpsu-monitor
WORKDIR /home/py-hpsu-monitor

FROM base as build

ADD --chown=py-hpsu-monitor https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py ./
RUN python get-poetry.py

RUN mkdir -p src/py_hpsu_monitor src/etc
COPY poetry.lock pyproject.toml ./src/
COPY etc ./src/etc/
COPY py_hpsu_monitor ./src/py_hpsu_monitor/
RUN cd ./src \
  && ~/.poetry/bin/poetry build --format wheel

FROM base

COPY --from=build "/home/py-hpsu-monitor/src/dist/py_hpsu_monitor-*-py3-none-any.whl" ./
RUN pip install --user $(ls py_*.whl)

ENTRYPOINT ["/home/py-hpsu-monitor/.local/bin/py-hpsu-monitor"]

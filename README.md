# py-hpsu-monitor

[![license](https://img.shields.io/github/license/weltenwort/py-hpsu-monitor?style=flat-square)](LICENSE)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
![test-status](https://img.shields.io/github/workflow/status/weltenwort/py-hpsu-monitor/Run%20tests?label=tests)

A bridge between the Rotex HPSU CAN bus and MQTT-based monitoring systems.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Background

This is intended to be deployed on a device that has a physical CAN connection
to a Rotex HPSU heating system. It polls a configurable set of registers via
the Elster-Kromschröder protocol and forwards the received values via MQTT. It
has only been tested with the following models:

- Rotex HPSU compact 508

Please contribute experiences with this or other models in an [issue].

## Install

To deploy from source use [poetry] to install or build a wheel.

## Usage

The configuration file allows for parameterization of various aspects:

- the CAN connection
- the MQTT connection
- the Elster protocol registers to poll

## Contributing

I welcome requests, bug reports and PRs.

Small note: If editing the Readme, please conform to the
[standard-readme](https://github.com/RichardLitt/standard-readme)
specification.

## License

[MIT](LICENSE)


[issue]: https://github.com/weltenwort/py-rotex-monitor/issues/new
[poetry]: https://python-poetry.org/

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

The application may be deployed from source or as a container. In both cases, make a copy of the `default-config.toml` file, change the settings to suit your deployment scenario, and specify the custom configuration file when starting the program.

### From source

To deploy from source use [poetry] to install or build a wheel.

The program itself can started by specifying the `run` command. The recommended usage is via the systemd unit file described below. Usually only the `--config-file` option will have to be sepecified for it to use the correct mqtt settings:

```
Usage: py-hpsu-monitor run [OPTIONS]

Options:
  --can-interface TEXT            CAN bus interface to monitor  [default:
                                  can0]
  --config-file FILE
  --register-definition-file FILE
                                  [default: /home/py-hpsu-
                                  monitor/.local/lib/python3.9/site-packages/p
                                  y_hpsu_monitor/elster_protocol/register_defi
                                  nitions.toml]
  --log-frames
  --log-registers
  --help                          Show this message and exit.
```

The commandline arguments and configuration file allows for parameterization of various aspects:

- the CAN connection
- the MQTT connection
- the Elster protocol registers to poll

### As a container

The included `Dockerfile` contains build instructions for an image based on Alpine Linux. The recommended way to build and deploy it is [podman]:

```
$ podman build --rm -t py-hpsu-monitor:latest .
```

#### With systemd and CAN interface `can0`

If your OS uses [systemd] as the supervisor you can use the included systemd unit to let it supervise the container for you:

- Copy `etc/py-hpsu-monitor.service` to `~/.config/systemd/user/py-hpsu-monitor.service` and potentially adjust the path to the configuration file.
- Copy `etc/socketcan@.service` to `/etc/systemd/system/socketcan@.service`.
- Enable both units:

  ```
  sudo systemctl enable --now socketcan@can0.service
  systemctl --user enable --now py-hpsu-monitor.service
  ```

#### Without systemd

To manually start the container without any supervision, make sure the socketcan interface is up and run sometime like:

```
$ podman run \
  --detach \
  --cgroups=no-conmon \
  --network=host \
  --volume $(pwd)/my-config.toml:/home/py-hpsu-monitor/config.toml:ro \
  localhost/py-hpsu-monitor:latest --config-file config.toml
```

## Contributing

I welcome requests, bug reports and PRs.

Small note: If editing the Readme, please conform to the
[standard-readme](https://github.com/RichardLitt/standard-readme)
specification.

## License

[MIT](LICENSE)

[issue]: https://github.com/weltenwort/py-rotex-monitor/issues/new
[poetry]: https://python-poetry.org/
[podman]: https://podman.io/

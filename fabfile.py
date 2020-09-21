import pathlib

from fabric import task

project_name = "py-hpsu-monitor"


@task
def deploy_source(c, version):
    versioned_project_name = f"{project_name}-{version}"
    source_archive_basename = f"{versioned_project_name}.tar.gz"
    source_archive_path = pathlib.Path("dist", source_archive_basename)
    c.put(source_archive_path, source_archive_basename)
    c.run(
        f"if [ -e '{versioned_project_name}' ]; then rm -R {versioned_project_name}; fi"
    )
    c.run(f"tar -xzf {source_archive_basename}")
    with c.cd(versioned_project_name):
        c.run("~/.poetry/bin/poetry env use 3.7")
        c.run("~/.poetry/bin/poetry install --no-dev --no-root")


@task
def deploy_wheel(c, wheel_path):
    wheel_basename = pathlib.Path(wheel_path).name
    c.put(wheel_path, wheel_basename)
    c.run(f".local/bin/pipx install --force ./{wheel_basename}")

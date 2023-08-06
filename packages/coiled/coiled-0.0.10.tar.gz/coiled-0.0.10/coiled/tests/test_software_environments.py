from distutils.util import strtobool
import io
import os
import platform
import yaml

import pytest
from distributed.utils_test import loop  # noqa: F401
from dask.distributed import Client

from coiled import CoiledCluster
from backends import in_process
from resources.apps import ResourcesConfig

from .conftest import ACCOUNT, CONFIGURATION


def skip_in_process_backend_not_on_linux():
    if (
        isinstance(ResourcesConfig.backend, in_process.ClusterManager)
        and platform.system() != "Linux"
    ):
        pytest.skip("TODO: allow for conda solve + build on non-linux platforms")


@pytest.mark.asyncio
async def test_update_software_environment_conda(cloud, cleanup, sample_user, tmp_path):
    skip_in_process_backend_not_on_linux()
    # below is what yaml.load(<env-file>) gives
    out = io.StringIO()
    conda_env = {
        "channels": ["defaults"],
        "dependencies": [
            "dask==2.15",
            "xarray",
            "pandas",
            # TODO is this how we want to handle pip installs within conda?
            # {"pip": ["numpy", "matplotlib"]},
        ],
    }

    await cloud.create_software_environment(name="env-1", conda=conda_env)

    await cloud.create_software_environment(
        name="env-1", conda=conda_env, log_output=out
    )

    out.seek(0)
    assert out.read().strip() == "Found built software environment"

    conda_env = {
        "channels": ["defaults"],
        "dependencies": ["dask", "xarray", "pandas",],
    }

    await cloud.create_software_environment(
        name="env-1", conda=conda_env, log_output=out
    )

    out.seek(0)
    text = out.read()
    assert "conda" in text.lower()
    assert "success" in text.lower() or "solved" in text.lower()


@pytest.mark.asyncio
async def test_update_software_environment_failure_doesnt_change_db(
    cloud, cleanup, sample_user, tmp_path
):
    skip_in_process_backend_not_on_linux()
    before_envs = await cloud.list_software_environments()
    out = io.StringIO()
    conda_env = {
        "channels": ["defaults"],
        "dependencies": ["dask", "not-a-package", "pandas",],
    }
    with pytest.raises(Exception):
        await cloud.create_software_environment(
            name="env-1", conda=conda_env, log_output=out
        )
    out.seek(0)
    text = out.read()
    assert "failed" in text.lower()
    after_envs = await cloud.list_software_environments()
    assert before_envs == after_envs


@pytest.mark.xfail(reason="TODO: support pip software environments", strict=True)
@pytest.mark.asyncio
async def test_software_environment_pip(cloud, cleanup, sample_user, tmp_path):

    packages = ["dask==2.15", "xarray", "pandas"]
    # Provide a list of packages
    await cloud.create_software_environment(name="env-1", pip=packages)

    result = await cloud.list_software_environments()
    # Check output is formatted properly
    expected = {
        "env-1": {"account": ACCOUNT, "spec": "\n".join(packages), "spec_type": "pip"}
    }
    assert result == expected


@pytest.mark.asyncio
async def test_software_environment_conda(cloud, cleanup, sample_user, tmp_path):
    skip_in_process_backend_not_on_linux()
    # below is what yaml.load(<env-file>) gives
    conda_env = {
        "channels": ["conda-forge"],
        "dependencies": [
            "dask=2.15",
            "xarray",
            "pandas",
            # TODO: support pip packages within a conda environment file
            # conda supports this via their CLI, but not when using conda.api.Solver
            # {"pip": ["numpy", "matplotlib"]},
        ],
    }

    # Provide a data structure
    await cloud.create_software_environment(name="env-1", conda=conda_env)

    result = await cloud.list_software_environments()

    # Check output is formatted properly
    assert len(result) == 1
    assert result["env-1"]["account"] == ACCOUNT
    assert result["env-1"]["spec"] == str(conda_env)
    assert result["env-1"]["spec_type"] == "conda"

    # Provide a local environment file
    environment_file = tmp_path / "environment.yml"
    with environment_file.open(mode="w") as f:
        f.writelines(yaml.dump(conda_env))

    await cloud.create_software_environment(name="env-2", conda=environment_file)

    result = await cloud.list_software_environments()

    # Check output is formatted properly
    assert len(result) == 2
    assert result["env-2"]["account"] == ACCOUNT
    assert result["env-2"]["spec"] == str(conda_env)
    assert result["env-2"]["spec_type"] == "conda"


@pytest.mark.asyncio
async def test_software_environment_container(cloud, cleanup, sample_user, tmp_path):

    # Provide docker image URI
    await cloud.create_software_environment(
        name="env-1", container="daskdev/dask:latest"
    )

    result = await cloud.list_software_environments()

    assert "env-1" in result
    assert "daskdev/dask:latest" in str(result)
    assert "container" in str(result)
    assert ACCOUNT in str(result)


@pytest.mark.asyncio
async def test_delete_software_environment(cloud, cleanup, sample_user):
    skip_in_process_backend_not_on_linux()
    # Initially no software environments
    result = await cloud.list_software_environments()
    assert not result

    packages = ["dask==2.15", "xarray", "pandas"]

    # Create two configurations
    await cloud.create_software_environment(name="env-1", conda=packages)
    await cloud.create_software_environment(name="env-2", conda=packages)

    result = await cloud.list_software_environments()
    assert len(result) == 2

    # Delete one of the configurations
    await cloud.delete_software_environment(name="env-1")
    result = await cloud.list_software_environments()
    assert len(result) == 1
    assert "env-2" in result


@pytest.mark.asyncio
async def test_docker_images(cloud, cleanup, sample_user, tmp_path, backend):
    if isinstance(backend, in_process.ClusterManager):
        raise pytest.skip()

    await cloud.create_software_environment(
        name="env-1",
        conda={
            "channels": ["conda-forge", "defaults"],
            "dependencies": ["python=3.8", "dask=2.19.0", "sparse"],
        },
    )
    await cloud.create_cluster_configuration(
        name=CONFIGURATION, software="env-1", worker_cpu=1, worker_memory="2 GiB",
    )

    async with CoiledCluster(asynchronous=True, configuration=CONFIGURATION) as cluster:
        async with Client(cluster, asynchronous=True) as client:

            def test_import():
                try:
                    import sparse  # noqa: F401

                    return True
                except ImportError:
                    return False

            result = await client.run_on_scheduler(test_import)
            assert result


@pytest.mark.asyncio
async def test_conda_raises(cloud, cleanup, sample_user, tmp_path):
    conda_env = {
        "channels": ["defaults"],
        "dependencies": ["dask", "not-a-package", "pandas",],
    }

    out = io.StringIO()
    with pytest.raises(Exception):
        await cloud.create_software_environment(
            name="env-1", conda=conda_env, log_output=out
        )
    out.seek(0)
    text = out.read()
    assert "failed" in text.lower()
    assert "not-a-package" in text.lower()


@pytest.mark.xfail(reason="this actually works if you have OpenGL available")
@pytest.mark.skipif(
    not strtobool(os.environ.get("TEST_AGAINST_AWS", "n")),
    reason="only fails on containers without OpenGL",
)
@pytest.mark.asyncio
async def test_docker_build_reports_failure(cloud, cleanup, sample_user, tmp_path):
    """ Sometime the docker build can fail, even if the conda solve works """
    skip_in_process_backend_not_on_linux()
    before_envs = await cloud.list_software_environments()
    out = io.StringIO()
    conda_env = {
        "channels": ["conda-forge"],
        "dependencies": ["napari"],
    }
    with pytest.raises(Exception):
        await cloud.create_software_environment(
            name="env-1", conda=conda_env, log_output=out
        )
    out.seek(0)
    text = out.read()
    assert "Missing OpenGL driver" in text
    assert "failed" in text.lower()

    after_envs = await cloud.list_software_environments()
    assert before_envs == after_envs

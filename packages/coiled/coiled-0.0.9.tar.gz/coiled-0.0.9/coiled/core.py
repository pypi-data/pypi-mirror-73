import asyncio
import json
import pathlib
import sys
from typing import Tuple, Union
import warnings
import weakref
import yaml

import aiobotocore
import aiohttp
import botocore.exceptions
import toolz
from tornado.ioloop import IOLoop

import dask
import dask.distributed
from distributed.utils import thread_state, sync, LoopRunner

from .utils import GatewaySecurity, handle_credentials
from .identifiers import parse_identifier


def delete_docstring(func):
    delete_doc = """ Delete a {kind}

Parameters
---------
name
    Name of {kind}.
account
    Name of the Coiled Cloud account which the {kind} belongs to.
    If not provided, will default to ``Cloud.default_account``.
"""
    func_name = func.__name__
    kind = " ".join(
        func_name.split("_")[1:]
    )  # delete_software_environments -> software environments
    func.__doc__ = delete_doc.format(kind=kind)
    return func


def list_docstring(func):

    list_doc = """ List {kind}s

Parameters
---------
account
    Name of the Coiled Cloud account to list {kind}s.
    If not provided, will default to ``Cloud.default_account``.

Returns
-------
:
    Dictionary with information about each {kind} in the
    specified account. Keys in the dictionary are names of {kind}s,
    while the values contain information about the corresponding {kind}.
"""
    func_name = func.__name__
    kind = " ".join(func_name.split("_")[1:])
    kind = kind[:-1]  # drop trailing "s"
    func.__doc__ = list_doc.format(kind=kind)
    return func


async def handle_api_exception(response):
    try:
        # First see if it's an error we created that has a more useful
        # message
        error_body = await response.json()
        if "message" in error_body:
            raise Exception(error_body["message"])
        # if message not in body, go back to our old parse text
    except (aiohttp.ContentTypeError, json.JSONDecodeError):
        pass

    error_text = await response.text()
    raise Exception(error_text)


class Cloud:
    """ Connect to Coiled Cloud

    Parameters
    ----------
    server
        Server to connect to. If not specified, will check the
        ``coiled.cloud.server`` configuration value.
    account
        The coiled account to use. If not specified,
        will check the ``coiled.cloud.account`` configuration value.
    asynchronous
        Set to True if using this Cloud within ``async``/``await`` functions or
        within Tornado ``gen.coroutines``. Otherwise this should remain
        ``False`` for normal use. Default is ``False``.
    loop
        If given, this event loop will be re-used, otherwise an appropriate one
        will be looked up or created.
    """

    _instances = weakref.WeakSet()
    _recent = list()

    def __init__(
        self,
        user: str = None,
        token: str = None,
        server: str = None,
        account: str = None,
        asynchronous: bool = False,
        loop: IOLoop = None,
    ):
        self.user = user or dask.config.get("coiled.cloud.user")
        self.token = token or dask.config.get("coiled.cloud.token")
        self.server = server or dask.config.get("coiled.cloud.server")
        if "://" not in self.server:
            self.server = "http://" + self.server
        self.server = self.server.rstrip("/")
        self._default_account = account or dask.config.get("coiled.cloud.account")
        self.session = None
        self.status = "init"
        self._asynchronous = asynchronous
        self._loop_runner = LoopRunner(loop=loop, asynchronous=asynchronous)
        self._loop_runner.start()

        Cloud._instances.add(self)
        Cloud._recent.append(weakref.ref(self))

        if not self.asynchronous:
            self._sync(self._start)

    def __repr__(self):
        return f"<Cloud: {self.user}@{self.server} - {self.status}>"

    def _repr_html_(self):
        text = (
            '<h3 style="text-align: left;">Coiled Cloud</h3>\n'
            '<ul style="text-align: left; list-style: none; margin: 0; padding: 0;">\n'
            f"  <li><b>User: </b>{self.user}</li>\n"
            f"  <li><b>Server: </b>{self.server}</li>\n"
            f"  <li><b>Account: </b>{self.default_account}</li>\n"
        )

        return text

    @property
    def loop(self):
        return self._loop_runner.loop

    @classmethod
    def current(cls, asynchronous=False):
        try:
            cloud = cls._recent[-1]()
            while cloud is None or cloud.status != "running":
                cls._recent.pop()
                cloud = cls._recent[-1]()
        except IndexError:
            try:
                return Cloud(asynchronous=asynchronous)
            except Exception:
                raise ValueError("Please first connect with coiled.Cloud(...)")
        else:
            return cloud

    @property
    def closed(self) -> bool:
        if self.session:
            return self.session.closed
        # If we haven't opened, we must be closed?
        return True

    async def _start(self):
        # Log in if we don't have a token
        if self.status != "init":
            return self
        if not self.token:
            self.user, self.token, self.server = await handle_credentials(
                server=self.server
            )

        self.session = aiohttp.ClientSession(
            headers={"Authorization": "Token " + self.token}
        )
        # do normal queries
        response = await self.session.request("GET", self.server + "/api/v1/users/me/")
        data = await response.json()
        if response.status >= 400:
            raise Exception(data)
        self.user = data["username"]
        self.accounts = {
            d["account"]["slug"]: toolz.merge(d["account"], {"admin": d["is_admin"]},)
            for d in data["membership_set"]
        }
        if self._default_account:
            self._verify_account(self._default_account)

        self.status = "running"

        return self

    @property
    def default_account(self):
        if self._default_account:
            return self._default_account
        elif len(self.accounts) == 1:
            return toolz.first(self.accounts)
        elif self.user in self.accounts:
            return self.user
        else:
            raise ValueError(
                "Please provide an account among the following options",
                list(self.accounts),
            )

    async def _close(self):
        if self.session:
            await self.session.close()
        self.status = "closed"

    def close(self):
        """ Close connection to Coiled Cloud
        """
        return self._sync(self._close)

    def __await__(self):
        return self._start().__await__()

    async def __aenter__(self):
        return await self._start()

    async def __aexit__(self, typ, value, tb):
        await self.close()

    def __enter__(self):
        return self

    def __exit__(self, typ, value, tb):
        self.close()

    @property
    def asynchronous(self) -> bool:
        """ Are we running in the event loop? """
        return self._asynchronous and self.loop is IOLoop.current()

    def _sync(self, func, *args, asynchronous=None, callback_timeout=None, **kwargs):
        if (
            asynchronous
            or self.asynchronous
            or getattr(thread_state, "asynchronous", False)
        ):
            future = func(*args, **kwargs)
            if callback_timeout is not None:
                future = asyncio.wait_for(future, callback_timeout)
            return future
        else:
            return sync(
                self.loop, func, *args, callback_timeout=callback_timeout, **kwargs
            )

    async def _list_clusters(self, account: str = None):
        account = account or self.default_account
        response = await self.session.request(
            "GET", self.server + "/api/v1/{}/clusters/".format(account),
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)

        data = await response.json()
        return {
            d["name"]: format_cluster_output(d)
            for d in data["results"]
            if d["status"] in ("pending", "running")
        }

    @list_docstring
    def list_clusters(self, account: str = None):
        return self._sync(self._list_clusters, account)

    async def _create_cluster(
        self, name: str, account: str = None, configuration: str = None
    ):
        account = account or self.default_account
        self._verify_account(account)
        data = {"name": name, "configuration": configuration}
        response = await self.session.request(
            "POST", self.server + "/api/v1/{}/clusters/".format(account), data=data,
        )
        if response.status >= 400:
            await handle_api_exception(response)

        return await response.json()

    def create_cluster(self, name: str, configuration: str, account: str = None):
        """ Create a cluster

        Parameters
        ---------
        name
            Name of cluster.
        configuration
            Identifier of the cluster configuration to use, in the format (<account>/)<name>. If the configuration
            is owned by the same account as that passed into "account", the (<account>/) prefix is optional.

            For example, suppose your account is "wondercorp", but your friends at "friendlycorp" have a configuration
            named "xgboost" that you want to use; you can specify this with "friendlycorp/xgboost". If you simply
            entered "xgboost", this is shorthand for "wondercorp/xgboost".
        account
            Name of the Coiled Cloud account to create the cluster in.
            If not provided, will default to ``Cloud.default_account``.

        See Also
        --------
        coiled.CoiledCluster
        """
        # TODO cleanup repetition of explaining a configuration identifier (see docstring for
        # creating software_environments)
        return self._sync(
            self._create_cluster,
            name=name,
            configuration=configuration,
            account=account,
        )

    async def _delete_cluster(self, name: str, account: str = None):
        account = account or self.default_account
        response = await self.session.request(
            "DELETE", self.server + "/api/v1/{}/clusters/{}/".format(account, name),
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)

    @delete_docstring
    def delete_cluster(self, name: str, account: str = None):
        return self._sync(self._delete_cluster, name, account)

    async def _cluster_status(self, name: str, account: str = None) -> dict:
        account = account or self.default_account
        response = await self.session.request(
            "GET", self.server + "/api/v1/{}/clusters/{}/".format(account, name),
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)

        data = await response.json()
        return data

    async def _security(
        self, name: str, account: str = None
    ) -> Tuple[dask.distributed.Security, dict]:
        while True:
            data = await self._cluster_status(name=name, account=account)
            if data["status"] != "pending":
                break
            else:
                await asyncio.sleep(1.0)

        security = GatewaySecurity(data["tls_key"], data["tls_cert"])

        return security, data

    def security(
        self, name: str, account: str = None
    ) -> Tuple[dask.distributed.Security, dict]:
        return self._sync(self._security, name, account)

    async def _connect(self, name: str, account: str = None) -> dask.distributed.Client:
        security, data = await self.security(name=name, account=account)  # type: ignore

        client = await dask.distributed.Client(
            data["public_address"],
            security=security,
            asynchronous=True,
            timeout="10 seconds",
        )
        async with aiobotocore.get_session().create_client("sts") as sts:
            try:
                credentials = await sts.get_session_token()
                credentials = credentials["Credentials"]
                # TODO: set up TTL, and update these credentials periodically

                await client.scheduler.aws_update_credentials(
                    credentials={
                        k: credentials[k]
                        for k in ["AccessKeyId", "SecretAccessKey", "SessionToken"]
                    }
                )
            except botocore.exceptions.NoCredentialsError:
                warnings.warn(
                    "No AWS credentials found -- none will be sent to the cluster."
                )

        return client

    def connect(self, name: str, account: str = None) -> dask.distributed.Client:
        """ Connect to a running cluster

        Parameters
        ----------
        name
            Name of cluster.
        account
            Name of Coiled Cloud account which the cluster belongs to.
            If not provided, will default to ``Cloud.default_account``.
        """
        return self._sync(self._connect, name, account)

    async def _scale(self, name: str, n: int, account: str = None) -> None:
        account = account or self.default_account
        response = await self.session.request(
            "PUT",
            self.server + "/api/v1/{}/clusters/{}/scale/".format(account, name),
            data={"count": n},
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)

    def scale(self, name: str, n: int, account: str = None) -> None:
        """ Scale cluster to ``n`` workers

        Parameters
        ----------
        name
            Name of cluster.
        n
            Number of workers to scale cluster size to.
        account
            Name of Coiled Cloud account which the cluster belongs to.
            If not provided, will default to ``Cloud.default_account``.
        """
        return self._sync(self._scale, name, n, account)

    def _verify_account(self, account: str):
        """ Perform sanity checks on account values

        In particular, this raises and informative error message if the
        account is not found, and provides a list of possible options.
        """
        account = account or self.default_account
        if account not in self.accounts:
            raise PermissionError(
                "Account not found: '{}'\n"
                "Possible accounts: {}".format(account, sorted(self.accounts))
            )

    def create_software_environment(
        self,
        name: str,
        conda: Union[list, dict, str] = None,
        container: str = None,
        log_output=sys.stdout,
    ) -> dict:
        """ Create a software environment

        Parameters
        ---------
        name
            Name of software environment.
        conda
            Specification for packages to install into the software environment using conda.
            Can be a list of packages, a dictionary, or a path to a conda environment YAML file.
        container
            Docker image to use for the software environment. Must be the name of a docker image
            on Docker hub.
        log_output
            Stream to output logs to. Defaults to ``sys.stdout``.

        Notes
        -----
        Exactly one of `conda`` or ``container`` must be specified.
        """
        return self._sync(
            self._create_software_environment,
            name=name,
            conda=conda,
            container=container,
            log_output=log_output,
        )

    async def _create_software_environment(
        self, name, conda=None, container=None, log_output=sys.stdout
    ):
        account, name = parse_identifier(name, "name")
        account = account or self.default_account

        # TODO: Eventually this should be v1/<str:account>/software_environments/<int:pk>
        if isinstance(conda, list):
            conda = {"dependencies": conda}
        elif isinstance(conda, (str, pathlib.Path)):
            # Local environment YAML file
            with open(conda, mode="r") as f:
                conda = yaml.safe_load(f)

        if (conda is None) + (container is None) != 1:
            raise ValueError(
                "Must specify exactly one of conda= or container= keywords.\n"
                "Got \n"
                "    conda={}\n"
                "    container={}".format(conda, container)
            )

        if conda:
            spec_type = "conda"
            spec = conda
        elif container:
            spec_type = "container"
            spec = container
        # TODO add other types as well

        # Connect to the websocket, send the data and get some logs
        data = {"new": spec, "spec_type": spec_type}
        # TODO shouldn't this be "wss" in production?
        ws_server = self.server.replace("http", "ws", 1)
        ws_endpoint = f"{ws_server}/ws/api/v1/{account}/software_environments/{name}/"

        try:
            ws = await self.session.ws_connect(ws_endpoint)
        except aiohttp.WSServerHandshakeError:
            raise ValueError(
                "Unable to connect to server, do you have permissions to "
                f'create environments in the "{account}" account?'
            )
        await ws.send_json(data)
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data.startswith("CLOSE_VIA_EXCEPTION"):
                    await ws.close()
                    raise ValueError(
                        f"Unable to update Environment:\n\n{msg.data[len('CLOSE_VIA_EXCEPTION: ') :]}"
                    )
                else:
                    print(f"{msg.data}", file=log_output)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break

    async def _list_software_environments(self, account=None):
        account = account or self.default_account
        response = await self.session.request(
            "GET", self.server + "/api/v1/{}/software_environments/".format(account),
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)
        else:
            results = (await response.json())["results"]
            results = {
                r["name"]: format_software_environment_output(r) for r in results
            }
            return results

    @list_docstring
    def list_software_environments(self, account=None) -> dict:
        return self._sync(self._list_software_environments, account=account)

    @delete_docstring
    def delete_software_environment(self, name, account=None):
        return self._sync(self._delete_software_environment, name, account=account,)

    async def _delete_software_environment(self, name, account=None):
        account = account or self.default_account
        response = await self.session.request(
            "DELETE", self.server + f"/api/v1/{account}/software_environments/{name}/",
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)

    def create_cluster_configuration(
        self,
        name: str,
        software: str,
        worker_cpu: int = 1,
        worker_memory: str = "4 GiB",
        scheduler_cpu: int = 1,
        scheduler_memory: str = "4 GiB",
    ) -> dict:
        """ Create a cluster configuration

        Parameters
        ----------
        name
            Name of cluster configuration.
            Optionally prefixed with an account name like "myaccount/myname"
        software
            Identifier of the software environment to use, in the format (<account>/)<name>. If the software environment
            is owned by the same account as that passed into "account", the (<account>/) prefix is optional.

            For example, suppose your account is "wondercorp", but your friends at "friendlycorp" have an environment
            named "xgboost" that you want to use; you can specify this with "friendlycorp/xgboost". If you simply
            entered "xgboost", this is shorthand for "wondercorp/xgboost".

            The "name" portion of (<account>/)<name> can only contain ASCII letters, hyphens and underscores.
        worker_cpu
            Number of CPUs allocated for each worker. Defaults to 1.
        worker_memory
            Amount of memory to allocate for each worker. Defaults to 4 GiB.
        scheduler_cpu
            Number of CPUs allocated for the scheduler. Defaults to 1.
        scheduler_memory
            Amount of memory to allocate for the scheduler. Defaults to 4 GiB.

        See Also
        --------
        dask.utils.parse_bytes
        """
        return self._sync(
            self._create_cluster_configuration,
            name=name,
            software=software,
            worker_cpu=worker_cpu,
            worker_memory=worker_memory,
            scheduler_cpu=scheduler_cpu,
            scheduler_memory=scheduler_memory,
        )

    async def _create_cluster_configuration(
        self,
        name: str,
        software: str,
        worker_cpu: int,
        worker_memory: str,
        scheduler_cpu: int,
        scheduler_memory: str,
    ):
        account, name = parse_identifier(name, "name")
        account = account or self.default_account

        response = await self.session.request(
            "POST",
            self.server + f"/api/v1/{account}/cluster_configurations/",
            data={
                "name": name,
                # "account": account,
                "software_environment": software,
                "worker_cpu": worker_cpu,
                "worker_memory": max(
                    # TODO we should be throwing an error instead of choosing
                    # 1 if they give use something below 1.
                    dask.utils.parse_bytes(worker_memory) // 2 ** 30,
                    1,
                ),
                "scheduler_cpu": scheduler_cpu,
                "scheduler_memory": max(
                    dask.utils.parse_bytes(scheduler_memory) // 2 ** 30, 1
                ),
                # TODO environments
            },
        )
        if response.status >= 400:
            await handle_api_exception(response)

    @list_docstring
    def list_cluster_configurations(self, account=None) -> dict:
        return self._sync(self._list_cluster_configurations, account=account)

    async def _list_cluster_configurations(self, account=None):
        account = account or self.default_account
        response = await self.session.request(
            "GET", self.server + f"/api/v1/{account}/cluster_configurations/",
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)
        else:
            results = (await response.json())["results"]
            results = {
                r["name"]: format_cluster_configuration_output(r) for r in results
            }
            return results

    @delete_docstring
    def delete_cluster_configuration(self, name):
        return self._sync(self._delete_cluster_configuration, name)

    async def _delete_cluster_configuration(self, name):
        if "/" in name:
            account, name = name.split("/")
        else:
            account = self.default_account
        response = await self.session.request(
            "DELETE", self.server + f"/api/v1/{account}/cluster_configurations/{name}/",
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)


# Utility functions for formatting list_* endpoint responses to be more user-friendly


def format_account_output(d):
    return d["slug"]


def format_software_environment_output(d):
    d = d.copy()
    d.pop("id")
    d.pop("name")
    d["account"] = format_account_output(d["account"])
    return d


def format_cluster_configuration_output(d):
    d = d.copy()
    d.pop("id")
    d.pop("name")
    d["account"] = format_account_output(d["account"])
    for process in ["scheduler", "worker"]:
        d[process].pop("id")
        d[process].pop("name")
        d[process].pop("account")
        d[process]["software"] = "/".join(
            [
                d[process]["software_environment"]["account"]["slug"],
                d[process]["software_environment"]["name"],
            ]
        )
    return d


def format_cluster_output(d):
    d = d.copy()
    for key in ["auth_token", "preload_key", "private_address", "name", "last_seen"]:
        d.pop(key)
    d["account"] = format_account_output(d["account"])
    # Rename "public_address" to "address"
    d["address"] = d["public_address"]
    d.pop("public_address")
    return d

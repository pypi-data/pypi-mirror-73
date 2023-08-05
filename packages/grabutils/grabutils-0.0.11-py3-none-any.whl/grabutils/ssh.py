import base64
import tempfile
from datetime import datetime
import os
from contextlib import contextmanager
from pathlib import Path

from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient


@contextmanager
def scp(ssh_client: SSHClient):
    yield SCPClient(ssh_client.get_transport())


@contextmanager
def ssh(server):
    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(
        server.host,
        username=server.user,
        key_filename=server.key_filename,
        look_for_keys=True,
        timeout=5000
    )
    try:
        yield client
    finally:
        client.close()


@contextmanager
def ssh_key(key, pub_key, key_fname):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_dir = Path(tmpdir)
        key_file = tmp_dir.joinpath(key_fname)
        with key_file.open('wb') as wh:
            wh.write(base64.b64decode(key.encode('utf8')))

        pubkey_file = tmp_dir.joinpath(key_fname + '.pub')
        with pubkey_file.open('wb') as wh:
            wh.write(base64.b64decode(pub_key.encode('utf8')))

        try:
            yield str(key_file)
        finally:
            pass


class RemoteServer:
    def __init__(self, host: str, user: str, key_filename: str):
        self.host = host
        self.user = user
        self.key_filename = key_filename

    def get(self, *args, **kwargs):
        with ssh(self) as client:
            with scp(client) as cp:
                cp.get(*args, **kwargs)

    def put(self, *args, **kwargs):
        with ssh(self) as client:
            with scp(client) as cp:
                cp.put(*args, **kwargs)

    @staticmethod
    def tstamp():
        return datetime.utcnow().strftime('%Y%m%d.%H%M%S')


@contextmanager
def ssh_cfg(alias=None):
    ssh_user = os.getenv('SSH_USER')
    ssh_host = os.getenv('SSH_HOST')
    ssh_alias = alias or ssh_host
    ssh_pkey = base64.b64decode(os.getenv('SSH_KEY'))
    ssh_pub_key = base64.b64decode(os.getenv('SSH_PUB_KEY'))
    ssh_key_fname = os.getenv('SSH_KEY_FILE')

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_ = Path(tmpdir)

        pkey_path = tmpdir_.joinpath(ssh_key_fname)
        pubkey_path = tmpdir_.joinpath(ssh_key_fname + '.pub')
        conf_path = tmpdir_.joinpath('config')

        with pkey_path.open('wb') as wh:
            wh.write(ssh_pkey)

        with pubkey_path.open('wb') as wh:
            wh.write(ssh_pub_key)

        with conf_path.open('w') as wh:
            wh.write(f'''
Host {ssh_alias}
    IdentitiesOnly  yes
    AddKeysToAgent  yes
    HostName        {ssh_host}
    User            {ssh_user}
    IdentityFile    {pkey_path}
''')

        yield str(conf_path)

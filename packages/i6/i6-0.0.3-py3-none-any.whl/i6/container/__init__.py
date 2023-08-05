from i6.container import ContainerCommand
from i6.log import log
from i6.util import util

import docker


class container():
    """
        Class for standardized container scripts.

        Example:
        ```
        # Attempt to use Dockerfile in cwd
        i6.container().run()

        # Use docker container from docker hub
        centos = i6.container({
            'name': 'centos',
            'image': 'centos:latest',
        })
        centos.run()

        # Example of all available settings
        all_config_options = i6.container({
            'name': 'all_config_options',
            'image': 'centos:latest',
            'remove': True,
            'restart': False,
            'ports': {
                '80/tcp': ('0.0.0.0', 8080),
            },
            'volumes': {
                'db': {'bind': '/var/lib/mysql', 'mode': 'rw'},
            },
            'env ': [
                f"MYSQL_ROOT_PASSWORD={i6.crypto.password()}",
                'MYSQL_DATABASE=wordpress'
            ],
            'init_build': True,
            'cmd': ['sh', '-c', '/root/init.sh; bash'],
        })
        all_config_options.run()
    """

    def __init__(self, obj = {}):
        if not isinstance(obj, dict):
            raise ValueError('container takes a dict')

        self.test = 'test'
        self.__obj = obj
        self.__client = container.client()
        
        self.__name = util.check_val(self.__obj, 'name', '')

        self.__image = util.check_val(self.__obj, 'image', None)
        self.__path = util.check_val(self.__obj, 'path', '.')

        if self.__image is not None:
            self.__path = None

        self.__remove = util.check_val(self.__obj, 'remove', True)

        if util.check_val(self.__obj, 'restart', False):
            self.__restart = {'Name': 'always'}
            self.__remove = False
        else:
            self.__restart = {}

        self.__ports = util.check_val(self.__obj, 'ports', {})
        self.__volumes = util.check_val(self.__obj, 'volumes', {})
        self.__env = util.check_val(self.__obj, 'env', [])
        self.__cmd = util.check_val(self.__obj, 'cmd', [])
        self.__init_build = util.check_val(self.__obj, 'init_build', True)

        try:
            self.__c = self.__client.containers.get(self.__name)
        except Exception:
            self.__c = None

        if self.__init_build:
            self.__build = ContainerCommand.ContainerCommandBuild(self).exec()

    def run(self):
        """
            Run the container

            Example:
            ```
            i6.container().run()
            ```
        """

        if not self.__init_build:
            self.__build = ContainerCommand.ContainerCommandBuild(self).exec()

        self.__c = ContainerCommand.ContainerCommandRun(self).exec()
        return self.__c

    def rm(self):
        """
            Remove container

            Example:
            ```
            centos = i6.container()
            centos.run()
            centos.rm()
            ```
        """

        return ContainerCommand.ContainerCommandRemove(self).exec()

    def stop(self):
        """
            Stop the container

            Example:
            ```
            centos = i6.container()
            centos.run()

            print(i6.container.ls())

            centos.stop()
            ```
        """

        return ContainerCommand.ContainerCommandStop(self).exec()

    def logs(self):
        """
            Get logs from container

            Example:
            ```
            centos = i6.container()
            centos.run()
            print(centos.logs())
            ```
        """

        return ContainerCommand.ContainerCommandLogs(self).exec()

    def info(self):
        """
            Get info stats from container

            Example:
            ```
            centos = i6.container()
            centos.run()
            print(centos.info())
            ```
        """

        return ContainerCommand.ContainerCommandInfo(self).exec()

    def client():
        """
            Get docker client

            Example:
            ```
            client = i6.container.client()
            for container in client.containers.list():
                print(container.id)
            ```
        """

        return docker.from_env()

    def ls():
        """
            List all containers

            Example:
            ```
            print(i6.container.ls())
            ```
        """

        client = container.client()

        try:
            result = []
            for c in client.containers.list():
                result.append(c.name)
            return result
        except docker.errors.APIError as e:
            log(e).stderr()

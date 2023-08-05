from i6 import errors
from i6.log import log

import docker


class ContainerCommand():
    def __init__(self, caller):
        self.caller = caller

    def template(self):
        pass

    def template_return(self):
        return True

    def exec(self):
        try:
            if self.caller._container__c is None:
                raise errors.ContainerIsNone()

            text = self.template()

            self.log_info(text)
            
            return self.template_return()
        except (docker.errors.APIError, errors.ContainerIsNone) as e:
            log(e).stderr()
        except Exception as e:
            log(f"Docker {e}").stderr()
        return None

    def log_info(self, text):
        if text is not None:
            log(f"{self.caller._container__name} {text}").stdout()

class ContainerCommandBuild(ContainerCommand):
    def __init__(self, caller):
        if caller._container__c is None:
            caller._container__c = dict()
        super().__init__(caller)

        self.__image = None

    def template(self):
        if self.caller._container__path is None:
            return
        
        self.log_info('Building')

        self.__image = self.caller._container__client.images.build(
            path = self.caller._container__path,
            tag = self.caller._container__name,
            rm = True,
            pull = True,
        )[0]

        return 'Built'
    
    def template_return(self):
        return self.__image

class ContainerCommandRun(ContainerCommand):
    def __init__(self, caller):
        if caller._container__c is None:
            caller._container__c = dict()
        super().__init__(caller)

        self.__c = None

    def template(self):
        self.__c = self.caller._container__c

        if self.caller._container__image is None:
            self.__image = self.caller._container__build
        else:
            self.__image = self.caller._container__image

        if self.__image is None:
            return

        if (self.__c is None) or (isinstance(self.__c, dict)):
            self.log_info('Starting')

            self.__c = self.caller._container__client.containers.run(
                name = self.caller._container__name,
                image = self.__image,
                remove = self.caller._container__remove,
                restart_policy = self.caller._container__restart,
                ports = self.caller._container__ports,
                volumes = self.caller._container__volumes,
                environment  = self.caller._container__env,
                command = self.caller._container__cmd,
                detach = True,
                tty = True,
                stdin_open = True,
            )
        else:
            self.__c.start()

        return 'Started'
    
    def template_return(self):
        return self.__c

class ContainerCommandStop(ContainerCommand):
    def __init__(self, caller):
        super().__init__(caller)

    def template(self):
        try:
            self.log_info('Stopping')
            self.caller._container__c.stop()
            return 'Stopped'
        except (docker.errors.APIError, AttributeError):
            raise errors.ContainerIsNone()

class ContainerCommandRemove(ContainerCommand):
    def __init__(self, caller):
        super().__init__(caller)

    def template(self):
        ContainerCommandStop(self.caller).exec()

        try:
            self.caller._container__c.remove()
            return 'Removed'
        except (docker.errors.APIError, AttributeError):
            raise errors.ContainerIsNone()

class ContainerCommandLogs(ContainerCommand):
    def __init__(self, caller):
        super().__init__(caller)
        self.__logs = None

    def template(self):
        self.__logs = self.caller._container__c.logs()

    def template_return(self):
        return self.__logs

class ContainerCommandInfo(ContainerCommand):
    def __init__(self, caller):
        super().__init__(caller)
        self.__stats = None

    def template(self):
        try:
            self.__stats = self.caller._container__c.stats(stream = False)
        except (ValueError, AttributeError, docker.errors.APIError):
            raise errors.ContainerIsNone()

    def template_return(self):
        return self.__stats

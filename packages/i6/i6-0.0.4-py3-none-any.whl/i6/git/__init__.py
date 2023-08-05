from i6.shell import shell
from i6.util import util

from setuptools._vendor.packaging import version


class git():
    """
        Class for standardized git scripts.

        Example:
        ```
        i6.git({
            'url': 'https://github.com/kruserr/i6',
        }).clone()

        centos = i6.container({
            'name': 'centos',
            'image': 'centos:latest',
        })
        centos.run()
        
        i6.git({
            'container': centos,
        }).update()
        ```
    """

    def __init__(self, obj = {}):
        self.__url = util.check_val(obj, 'url', None)
        self.__container = util.check_val(obj, 'container', None)

    def update(self):
        """
            Update git repo in cwd to the latest tag.

            Example:
            ```
            centos = i6.container({
            'name': 'centos',
            'image': 'centos:latest',
            })
            centos.run()
            
            i6.git({
                'container': centos,
            }).update()
            ```
        """
        
        current = self.__get_latest_tag()

        current_branch = shell.exec(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])

        if current_branch != 'master':
            shell.exec(['git', 'checkout', 'master'])

        shell.exec(['git', 'pull'])

        newest = self.__get_latest_tag()

        if current < newest:
            shell.exec(['git', 'checkout', self.__get_latest_tag(False)])
            self.__container.rm()
            self.__container.run()
    
    def clone(self):
        """
            Clone a git repository in cwd

            Example:
            ```
            i6.git({
                'url': 'https://github.com/kruserr/i6',
            }).clone()
            ```
        """

        if self.__url is not None:
            print(f"cloning {self.__url}")

    def __get_latest_tag(self, parse = True):
        rev_list = shell.exec(['git', 'rev-list', '--tags', '--max-count=1'])
        describe = shell.exec(['git', 'describe', '--tags', rev_list])

        if parse:
            return version.parse(describe)
        return describe

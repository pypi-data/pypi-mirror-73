from i6.cli.main import main

import os
import argparse


class cli():
    """
        Class to interact with the program using the CLI.

        Example:
        ```
        i6.cli().run()
        ```

        This class allows for a interactive CLI experiance,
        and also a no menu option where it is more suited
        to be used for scripting in python.
    """

    def __init__(self, func_args = '', menu = True):
        parser = argparse.ArgumentParser(description='i6')

        parser.add_argument(
            'tool', metavar='tool', type=str, default='', nargs='*',
            help='Select a tool to use',
        )

        if len(func_args) == 0:
            try:
                self.__args = parser.parse_args()
            except:
                self.__args = parser.parse_args(func_args.split())
        else:
            self.__args = parser.parse_args(func_args.split())
        
        self.__exit = False
        self.__menu = menu

    def __clear_console(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def __get_header(self, text):
        def wrap():
            result = ''
            for _ in range(len(text) + 4):
                result += '#'
            return result
        
        return f"{wrap()}\n# {text} #\n{wrap()}\n\n"
    
    def __func_menu(self):
        if len(self.__args.tool) == 0:
            select = ''
            while select != '0':
                self.__clear_console()
                print(f"{self.__get_header('i6')}\n[1] - Select tool\n[0] - Exit\n")

                select = input()
                
                if select == '0':
                    self.__exit = True
                    return
                
                if select == '1':
                    self.__clear_console()
                    print(f"{self.__get_header('Select tool')}")

                    inner_select = input('Enter a tool: ')
                    self.__args.tool = inner_select

    def run(self):
        if self.__menu:
            self.__func_menu()

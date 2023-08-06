import html2text
import os
import requests
import sys


class Fmt:
    BLACK = '\u001b[30m'
    RED = '\u001b[31m'
    YELLOW = '\u001b[33m'
    GREEN = '\u001b[32m'
    BLUE = '\u001b[34m'
    MAGENTA = '\u001b[35m'
    CYAN = '\u001b[36m'
    WHITE = '\u001b[37m'
    BRIGHT_BLACK = '\u001b[90m'
    BRIGHT_RED = '\u001b[91m'
    BRIGHT_YELLOW = '\u001b[93m'
    BRIGHT_BLUE = '\u001b[94m'
    BRIGHT_GREEN = '\u001b[92m'
    BRIGHT_MAGENTA = '\u001b[95m'
    BRIGHT_CYAN = '\u001b[96m'
    BRIGHT_WHITE = '\u001b[97m'

    @classmethod
    def to_color(self, color, text):
        return getattr(Fmt, color) + text


def help():
    return (
            f'''
    {Fmt.to_color('BRIGHT_YELLOW', 'Welcome to wiki.archlinux.org!')}

    {Fmt.to_color('BRIGHT_YELLOW', 'Usage')}:
        {Fmt.to_color('BRIGHT_CYAN',
        'archwiki option [SEARCH]')}    {Fmt.to_color('BRIGHT_WHITE',
        'returns the corresponding page from archwiki')}

    {Fmt.to_color('BRIGHT_GREEN', 'Options')}:
        {Fmt.to_color('BRIGHT_CYAN',
        '-p, --print')}                 {Fmt.to_color('BRIGHT_WHITE',
        'prints the page')}

        {Fmt.to_color('BRIGHT_CYAN',
        '-s, --save')}                  {Fmt.to_color('BRIGHT_WHITE',
        'saves the page (page_search.md) in your current directory')}

        {Fmt.to_color('BRIGHT_CYAN',
        '-h, --help')}                  {Fmt.to_color('BRIGHT_WHITE',
        'prints the current cli interface')}

    '''
    )


def not_found():
    return (
            f'''
    {Fmt.to_color('BRIGHT_YELLOW',
        'There were no results matching the query!')}

    {Fmt.to_color('BRIGHT_WHITE', 'Try again...')}

    '''
    )


def get_page(query: str):
    URL = 'https://wiki.archlinux.org/index.php?search='
    try:
        with requests.get(URL+query) as response:
            response.raise_for_status()
            data = response.text
        data = html2text.html2text(data)
        return data
    except requests.RequestException as error:
        message = str(error)
        print(message)


def main(args):
    data = get_page(args[2])
    MSG = 'There were no results matching the query'
    if data.find(MSG) != -1:
        print(not_found())
    else:
        print(data)
        if args[1] == '-s':
            sys.path.insert(1, os.getcwd())
            with open(f'page_{args[2]}.md', 'a') as page:
                page.write(data)
            print('\n\nPage saved!\n\n')


def run():
    args = sys.argv
    if len(args) != 3 or args[1] == '-h':
        print(help())
    else:
        main(args)

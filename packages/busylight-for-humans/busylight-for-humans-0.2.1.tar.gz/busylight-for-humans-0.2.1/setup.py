# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['busylight', 'busylight.lights']

package_data = \
{'': ['*']}

install_requires = \
['bitvector-for-humans>=0.12.0,<0.13.0',
 'hidapi>=0.9.0,<0.10.0',
 'typer>=0,<1',
 'webcolors>=1.11.1,<2.0.0']

entry_points = \
{'console_scripts': ['busylight = busylight.__main__:cli']}

setup_kwargs = {
    'name': 'busylight-for-humans',
    'version': '0.2.1',
    'description': 'Control USB connected LED lights, like a human.',
    'long_description': "# `busylight`\n\nControl USB attached LED lights like a Human™\n\n![Two Lights at Once](https://github.com/JnyJny/busylight/raw/master/demo/demo.gif)\n\nMake a supported USB attached LED light turn on, off and blink; all\nfrom the comfort of your very own command-line. If your platform\nsupports HIDAPI (Linux, MacOS, Windows and probably others), then\nyou can use `busylight`!\n\n## Usage\n\n\n```console\n$ busylight on\n$ busylight off\n$ busylight on purple\n$ busylight on 0xff00ff   # still purple.\n$ busylight blink yellow  # all hands man your stations.\n$ busylight blink red     # RED ALERT!\n$ busylight off           # all clear.\n```\n\n## Supported Lights\n\n\n```console\n$ busylight supported\nEmbrava BlyncLight\nLuxafor Flag\n```\n\n## Install\n\n\n```console\n$ pip install -U busylight-for-humans\n$ busylight --help\n```\n\n## Source\n\n\n[busylight](https://github.com/JnyJny/busylight.git)\n\n**Usage**:\n\n```console\n$ busylight [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `-l, --light-id INTEGER`: Which light to operate on, see list output.  [default: 0]\n* `-a, --all`: Operate on all lights.\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `blink`: Activate the selected light in blink mode.\n* `list`: List available lights (currently connected).\n* `off`: Turn selected lights off.\n* `on`: Turn selected lights on.\n* `supported`: List supported LED lights.\n\n## `busylight blink`\n\nActivate the selected light in blink mode.\n\nThe light selected will blink with the specified color. The default color is red\nif the user omits the color argument. Colors can be specified with color names and\nhexadecimal values. Both '0x' and '#' are recognized as hexidecimal number prefixes\nand hexadecimal values may be either three or six digits long. \n\nExamples:\n\n```console\n$ busylight blink          # light is blinking with the color red\n$ busylight blink green    # now it's blinking green\n$ busylight blink 0x00f    # now it's blinking blue\n$ busylight blink #ffffff  # now it's blinking white\n$ busylight --all blink    # now all available lights are blinking red\n$ busylight --all off      # that's enough of that!\n```\n\n**Usage**:\n\n```console\n$ busylight blink [OPTIONS] [COLOR]\n```\n\n**Options**:\n\n* `-s, --speed`: Blink speed\n* `--help`: Show this message and exit.\n\n## `busylight list`\n\nList available lights (currently connected).\n    \n    \n\n**Usage**:\n\n```console\n$ busylight list [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `busylight off`\n\nTurn selected lights off.\n\nTo turn off all lights, specify --all:\n\n```console\n$ busylight --all off\n```\n\n**Usage**:\n\n```console\n$ busylight off [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `busylight on`\n\nTurn selected lights on.\n\nThe light selected is turned on with the specified color. The default color is green\nif the user omits the color argument. Colors can be specified with color names and\nhexadecimal values. Both '0x' and '#' are recognized as hexidecimal number prefixes\nand hexadecimal values may be either three or six digits long. \n\nExamples:\n\n\n```console\n$ busylight on          # light activated with the color green\n$ busylight on red      # now it's red\n$ busylight on 0x00f    # now it's blue\n$ busylight on #ffffff  # now it's white\n$ busylight --all on    # now all available lights are green\n```\n\n**Usage**:\n\n```console\n$ busylight on [OPTIONS] [COLOR]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `busylight supported`\n\nList supported LED lights.\n    \n\n**Usage**:\n\n```console\n$ busylight supported [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n",
    'author': 'JnyJny',
    'author_email': 'erik.oshaughnessy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JnyJny/busylight.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

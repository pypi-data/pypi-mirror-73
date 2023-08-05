# Copyright 2019 The ASReview Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command Line Interface (CLI) for ASReview project."""
import argparse
import logging
import pkg_resources
import sys

from asreview import __version__


PROG_DESCRIPTION = f"""
Automated Systematic Review (ASReview).
"""


def main():
    # Find the available entry points.
    entry_points = {
        entry.name: entry
        for entry in pkg_resources.iter_entry_points('asreview.entry_points')
    }

    # Try to load the entry point if available.
    if len(sys.argv) > 1 and sys.argv[1] in entry_points:
        try:
            entry = entry_points[sys.argv[1]]
            entry.load()().execute(sys.argv[2:])
        except ModuleNotFoundError:
            raise ValueError(
                f"Plugin with entry point {entry.name} could not be loaded.")

    # Print help message if the entry point could not be found.
    else:
        description_list = []
        for name, entry in entry_points.items():
            try:
                description_list.append(entry.load()().format(name))
            except ModuleNotFoundError:
                logging.warning(
                    f"Plugin with entry point {name} could not be loaded.")

        description = "\n\n".join(description_list)
        parser = argparse.ArgumentParser(
            prog="asreview",
            formatter_class=argparse.RawTextHelpFormatter,
            description=PROG_DESCRIPTION
        )
        parser.add_argument(
            "subcommand",
            nargs="?",
            default=None,
            help=f"The subcommand to launch. Available commands:\n\n"
            f"{description}"
        )

        # version
        parser.add_argument(
            "-V", "--version",
            action='store_true',
            help="print the ASR version number and exit")

        args, _ = parser.parse_known_args()

        # output the version
        if args.version:
            print(__version__)
            return

        parser.print_help()


# execute main function
if __name__ == "__main__":
    main()

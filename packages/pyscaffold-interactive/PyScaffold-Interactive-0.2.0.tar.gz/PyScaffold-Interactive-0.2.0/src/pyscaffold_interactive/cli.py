# -*- coding: utf-8 -*-
"""
Interactively generate a Python project template with customizations
using PyScaffold
"""

import logging
import subprocess
from collections.abc import Iterable

import click
from pyscaffold import info, templates
from pyscaffold.api import create_project
from pyscaffold.extensions.pre_commit import PreCommit
from pyscaffold.extensions.tox import Tox
from pyscaffold.extensions.travis import Travis

# from pyscaffold_interactive import __version__

__author__ = "Sarthak Jariwala"
__copyright__ = "Sarthak Jariwala"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def prompt_text(text, default=None):
    """Prompt user text input
    """
    prompt_ans = click.prompt(click.style(text, fg="blue"), default=default)
    return prompt_ans


def prompt_choice(text, choices, default=None):
    """Prompt user input from provided choices
    """
    # choices must be iterable
    assert isinstance(choices, Iterable)

    prompt_ans = click.prompt(
        click.style(text, fg="blue"),
        show_choices=True,
        type=click.Choice(choices, case_sensitive=False),
        default=default,
    )

    return prompt_ans


@click.command()
def main():
    """Interactive Python/DataScience project template setup using PyScaffold
    """

    license_choices = templates.licenses.keys()
    extensions = []

    click.echo(
        click.style(
            "\nPyScaffold-Interactive - A tool to interactively "
            + "create python project templates using PyScaffold\n",
            fg="green",
        )
    )

    project_name = prompt_text("Enter your project name ", default="PyProject")

    author = prompt_text("Package author name ", default=info.username())

    email = prompt_text("Author email", default=info.email())

    url = prompt_text(
        "Project URL",
        default="https://github.com/SarthakJariwala/PyScaffold-Interactive",
    )

    description = prompt_text(
        "Enter package description\n",
        default="Generated using PyScaffold and PyScaffold-Interactive",
    )

    license = prompt_choice("Choose License\n", license_choices, default="mit").lower()

    is_data_sci_proj = prompt_choice(
        "Is this a DataScience project?", ["y", "n"], default="n"
    ).lower()

    if is_data_sci_proj == "y":
        data_sci_cmds = str(
            "putup '{}' --description '{}' --url '{}' --license '{}' --dsproject".format(
                project_name, description, url, license
            )
        )

    make_tox = prompt_choice(
        "Generate config files for automated testing using tox? ",
        ["y", "n"],
        default="y",
    ).lower()

    if make_tox == "y":
        if is_data_sci_proj == "y":
            data_sci_cmds += " --tox"
        else:
            extensions.append(Tox("tox"))

    create_travis = prompt_choice(
        "Generate config and script files for Travis CI.? ", ["y", "n"], default="y"
    ).lower()

    if create_travis == "y":
        if is_data_sci_proj == "y":
            data_sci_cmds += " --travis"
        else:
            extensions.append(Travis("travis"))

    # only ask for pre-commit if not datascience project, auto-yes for datasci project
    if is_data_sci_proj == "n":
        create_pre_commit = prompt_choice(
            "Generate pre-commit config? [Recommended] ", ["y", "n"], default="y"
        ).lower()

        if create_pre_commit == "y":
            extensions.append(PreCommit("pre-commit"))

    if is_data_sci_proj == "y":
        # setup datascience project using putup
        subprocess.check_output(data_sci_cmds, shell=True)  # need to test on windows
    else:
        create_project(
            project=project_name,
            license=license,
            extensions=extensions,
            opts={
                "description": "{}".format(description),
                "author": "{}".format(author),
                "email": "{}".format(email),
                "url": "{}".format(url),
            },
        )

    click.echo(
        click.style(
            "\nSuccess! {} created. Lets code!".format(project_name), fg="green"
        )
    )

    click.echo(
        click.style("\nAll putup commands are also available. For help - ", fg="green")
        + click.style("'putup --help'", fg="red")
    )


def run():
    """Entry point for console_scripts
    """
    main()


if __name__ == "__main__":
    run()

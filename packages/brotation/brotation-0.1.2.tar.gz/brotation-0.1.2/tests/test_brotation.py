#!/usr/bin/env python

"""Tests for `brotation` package."""


import pytest
import os

import yaml

from click.testing import CliRunner

from brotation import brotation
from brotation import cli

from gutools.tools import fileiter
from gutools.upytest import tempfolder, select_one


@pytest.fixture
def runner():
    runner = CliRunner()
    return runner


def test_cli_no_args(runner):
    """Test the CLI."""
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'backup' in result.output
    assert 'restore' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_cli_backup(runner, tempfolder):
    """Test the CLI."""
    foo = 1
    folders = os.path.dirname(__file__)
    cmdlines = [
        [f"--where={tempfolder}/test_1", f"--folders={folders}"],
        ['-w', f"{tempfolder}/test_2", f"-f {folders}"],
    ]
    for cmd in cmdlines:
        result = runner.invoke(cli.backup, cmd)
        if result.exit_code:
            print(result.output)
            raise RuntimeError(f'Error code: {result.exit_code}')
        else:
            # ok!, let's check that some tar files are created
            foo = 1
            for filename in fileiter(tempfolder, wildcard='*.tar.*'):
                break
            else:
                raise RuntimeError("Can not find a tar file after running test")

        #assert 'backup' in result.output
        #assert 'restore' in result.output
        #help_result = runner.invoke(cli.main, ['--help'])
        #assert help_result.exit_code == 0
        #assert '--help  Show this message and exit.' in help_result.output


def test_cli_backup_using_configfile(runner, tempfolder):
    """Test the CLI using config file.
    
    Example:
    
    $ cat brotator.yaml
    compression: xz
    folders:
    - /home/agp/Documents/me/code/brotation
    - /home/agp/Documents/me/code/gutools
    where: /mnt/brotation

"""
    # write a config file
    folders = os.path.dirname(__file__)
    config = {
        'where': f"{tempfolder}/test_1",
        'folders': [f"{folders}", '/tmp/kk2'],
        'compression': 'xz',
    }
    configfile = f"{tempfolder}/brotator.yaml"
    with open(configfile, 'wt') as f:
        yaml.dump(config, stream=f)

    # execute using config file
    cmdlines = [
        [f"--config={configfile}", ],
    ]

    for cmd in cmdlines:
        result = runner.invoke(cli.backup, cmd)
        if result.exit_code:
            print(result.output)
        else:
            # ok!
            pass
    foo = 1

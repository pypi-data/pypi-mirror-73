#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest

from import_git_files import GitExtractedFiles


def test_extracting_from_git(tmpdir):
    """
    Test that our git extractor works. Use a public git page for the
    test.
    """
    with GitExtractedFiles(
        git_url="https://github.com/sphinx-doc/sphinx",
        source_destination_map={
            "README.rst": os.path.abspath(os.path.join(tmpdir, "README.rst"))
        }
    ) as extracted:
        assert os.path.exists(extracted[0])
        with open(extracted[0], 'r') as file_handle:
            content = file_handle.read()
            assert 'Sphinx' in content


def test_extracting_branch_or_tag_from_git(tmpdir):
    """
    Test that our git extractor works on a tag/branch. Use a public git
    page for the test on a frozen release so the RELEASE/changelog top line
    should match that release tag.
    """
    with GitExtractedFiles(
        git_url="https://github.com/sphinx-doc/sphinx@v3.1.2",
        source_destination_map={
            "CHANGES": os.path.abspath(os.path.join(tmpdir, "CHANGES"))
        }
    ) as extracted:
        assert os.path.exists(extracted[0])
        with open(extracted[0], 'r') as file_handle:
            content = file_handle.readlines()
            assert '3.1.2' in content[0].lower()


def test_defining_multiple_authentication_methods(tmpdir):
    """
    Private registries require the user interactively login or
    non-interactively specify a github token or ssh deploy key. If both
    non-interactive methods are supplied, this should raise an error.
    """
    with pytest.raises(ValueError):
        with GitExtractedFiles(
            git_url="https://github.com/sphinx-doc/sphinx",
            ssh_key_path="/dev/null",
            token="token",
            source_destination_map={
                "CHANGES": os.path.abspath(os.path.join(tmpdir, "CHANGES"))
            }
        ) as extraction:
            assert os.path.exists(extraction[0])


def test_destination_with_parents_that_do_not_already_exist(tmpdir):
    """
    The GitExtractedFiles destination paths can contain parent
    directories that do not exist. It has a helper to create the parents if
    they do not. This sets a destination in a directory that is not already
    created before calling so it will test that it can succeed doing that.
    """
    with GitExtractedFiles(
        git_url="https://github.com/sphinx-doc/sphinx",
        source_destination_map={
            "README.rst": os.path.abspath(os.path.join(tmpdir,
                                                       "parent/README.rst"))
        }
    ) as extracted:
        assert os.path.exists(extracted[0])
        with open(extracted[0], 'r') as file_handle:
            content = file_handle.read()
            assert 'Sphinx' in content

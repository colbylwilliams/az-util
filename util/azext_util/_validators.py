# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from re import match
from knack.log import get_logger
from azure.cli.core.util import CLIError

logger = get_logger(__name__)

# pylint: disable=unused-argument, protected-access, import-outside-toplevel


def util_source_version_validator(cmd, ns):
    if ns.version:
        if ns.prerelease:
            raise CLIError(
                'usage error: can only use one of --version/-v | --pre')
        ns.version = ns.version.lower()
        if ns.version[:1].isdigit():
            ns.version = 'v' + ns.version
        if not _is_valid_version(ns.version):
            raise CLIError(
                '--version/-v should be in format v0.0.0 do not include -pre suffix')

        from ._utils import github_release_version_exists

        if not github_release_version_exists(ns.version):
            raise CLIError('--version/-v {} does not exist'.format(ns.version))


def _is_valid_url(url):
    return match(
        r'^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$', url) is not None


def _is_valid_version(version):
    return match(r'^v[0-9]+\.[0-9]+\.[0-9]+$', version) is not None

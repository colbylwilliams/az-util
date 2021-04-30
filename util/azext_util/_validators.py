# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from re import match
# from uuid import UUID
# from azure.cli.core.util import CLIError
from knack.log import get_logger

logger = get_logger(__name__)

# pylint: disable=unused-argument, protected-access


def _is_valid_url(url):
    return match(
        r'^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$', url) is not None


def _is_valid_version(version):
    return match(r'^v[0-9]+\.[0-9]+\.[0-9]+$', version) is not None

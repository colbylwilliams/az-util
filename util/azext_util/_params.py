# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ._validators import util_source_version_validator


def load_arguments(self, _):

    with self.argument_context('util update') as c:
        c.argument('version', options_list=['--version', '-v'], help='Version (tag). Default: latest stable.',
                   validator=util_source_version_validator)
        c.argument('prerelease', options_list=['--pre'], action='store_true',
                   help='Deploy latest prerelease version.')

    with self.argument_context('util group delete') as c:
        c.argument('prefix', options_list=['--prefix', '-p'],
                   help='Resource group name prefix (case insensitive).')
        c.argument('skip', options_list=['--skip', '-s'], nargs='*',
                   help='Space-separated resource groups to skip.')

    with self.argument_context('util keyvault purge') as c:
        c.argument('skip', options_list=['--skip', '-s'], nargs='*',
                   help='Space-separated keyvaults to skip.')

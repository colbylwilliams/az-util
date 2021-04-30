# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=too-many-statements
# pylint: disable=line-too-long
# from knack.arguments import CLIArgumentType
# from azure.cli.core.commands.parameters import tags_type, file_type


def load_arguments(self, _):

    with self.argument_context('util group delete') as c:
        c.argument('prefix', options_list=['--prefix', '-p'], help='Resource group name prefix (case insensitive).')
        c.argument('skip', options_list=['--skip', '-s'], nargs='*', help='Space-separated resource groups to skip.')

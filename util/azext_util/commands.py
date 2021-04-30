# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

def load_command_table(self, _):  # pylint: disable=too-many-statements

    with self.command_group('util', is_preview=True):
        pass

    with self.command_group('util') as g:
        g.custom_command('update', 'util_update')

    with self.command_group('util group') as g:
        g.custom_command('delete', 'group_delete')

    with self.command_group('util keyvault') as g:
        g.custom_command('purge', 'keyvault_purge')

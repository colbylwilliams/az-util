# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=unused-argument, protected-access, too-many-lines, import-outside-toplevel

from knack.log import get_logger
from knack.prompting import prompt_y_n
from knack.util import CLIError

from ._client_factory import (keyvault_client_factory, resource_client_factory,
                              resource_lock_client_factory)

logger = get_logger(__name__)


def util_update(cmd, version=None, prerelease=False):
    from azure.cli.core.extension.operations import update_extension

    from ._utils import get_github_release

    release = get_github_release(version=version, prerelease=prerelease)

    index = next((a for a in release['assets']
                  if 'index.json' in a['browser_download_url']), None)

    index_url = index['browser_download_url'] if index else None

    if not index_url:
        raise CLIError(
            f"Could not find index.json asset on release {release['tag_name']}. "
            'Specify a specific prerelease version with --version '
            'or use latest prerelease with --pre')

    update_extension(cmd, extension_name='util', index_url=index_url)


def group_delete(cmd, prefix, skip=None, force=False, yes=False):

    client = resource_client_factory(cmd.cli_ctx)
    lock_client = resource_lock_client_factory(cmd.cli_ctx)

    groups = client.resource_groups.list()
    groups = list(groups)

    to_delete = []
    skipped = []
    deleted = []

    for group in [group for group in groups if group.name.startswith(prefix)]:

        if skip and group.name in skip:
            logger.info('skipping resource group: %s', group.name)
            skipped.append(group)
            continue

        to_delete.append(group)

    if not to_delete:
        logger.info('no resource groups to delete match prefix %s', prefix)
        return deleted

    if not yes:
        logger.warning('\nWARNING: The following resource groups will be permanently deleted:')
        print('\n- {}'.format('\n- '.join([group.name for group in to_delete])))

    if not yes and not prompt_y_n('\nAre you sure you want to continue?', default='n'):
        return None

    for group in to_delete:

        if force:
            locks = lock_client.management_locks.list_at_resource_group_level(group.name)
            locks = list(locks)

            for lock in locks:
                logger.info('deleting lock: %s', lock.name)
                lock_client.management_locks.delete_at_resource_group_level(group.name, lock.name)

        logger.info('deleting resource group: %s', group.name)
        client.resource_groups.begin_delete(group.name)

        deleted.append(group)

    return deleted


def keyvault_purge(cmd, skip=None, yes=False):

    client = keyvault_client_factory(cmd.cli_ctx).vaults

    vaults = client.list_deleted()

    to_purge = []
    purged = []

    for vault in vaults:

        if skip and vault.name in skip:
            logger.info('skipping keyvault: %s', vault.name)
            continue

        to_purge.append(vault)

    if not to_purge:
        logger.info('no deleted keyvaults to purge')
        return to_purge

    if not yes:
        logger.warning('\nWARNING: The following key vaults will be permanently deleted:')
        print('\n- {}'.format('\n- '.join([vault.name for vault in to_purge])))

    if not yes and not prompt_y_n('\nAre you sure you want to continue?', default='n'):
        return None

    for vault in to_purge:

        logger.info('purging keyvault: %s', vault.name)
        client.begin_purge_deleted(vault.name, vault.properties.location)

        purged.append(vault)

    return purged

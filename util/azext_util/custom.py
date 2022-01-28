# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=unused-argument, protected-access, too-many-lines, import-outside-toplevel

from knack.log import get_logger
from knack.util import CLIError
from ._client_factory import (resource_client_factory,
                              resource_lock_client_factory,
                              keyvault_client_factory)

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


def group_delete(cmd, prefix, skip=None):

    client = resource_client_factory(cmd.cli_ctx)
    lock_client = resource_lock_client_factory(cmd.cli_ctx)

    groups = client.resource_groups.list()
    groups = list(groups)

    deleted = []

    for group in [group for group in groups if group.name.startswith(prefix)]:

        if skip and group.name in skip:
            logger.info('skipping resource group: %s', group.name)
            continue

        locks = lock_client.management_locks.list_at_resource_group_level(group.name)
        locks = list(locks)

        for lock in locks:
            logger.info('deleting lock: %s', lock.name)
            lock_client.management_locks.delete_at_resource_group_level(group.name, lock.name)

        logger.info('deleting resource group: %s', group.name)
        client.resource_groups.begin_delete(group.name)

        deleted.append(group)

    return deleted


def keyvault_purge(cmd, skip=None):

    client = keyvault_client_factory(cmd.cli_ctx).vaults

    vaults = client.list_deleted()

    purged = []

    for vault in vaults:

        if skip and vault.name in skip:
            logger.info('skipping keyvault: %s', vault.name)
            continue

        logger.info('purging keyvault: %s', vault.name)
        client.begin_purge_deleted(vault.name, vault.properties.location)

        purged.append(vault)

    return purged

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


def util_update(cmd, version=None, prerelease=False):  # pylint: disable=too-many-statements, too-many-locals
    import os
    import tempfile
    import shutil
    from azure.cli.core import CommandIndex
    from azure.cli.core.extension import get_extension
    from azure.cli.core.extension.operations import _add_whl_ext, _augment_telemetry_with_ext_info
    from ._utils import get_github_release

    release = get_github_release(version=version, prerelease=prerelease)
    asset = next((a for a in release['assets']
                  if 'py3-none-any.whl' in a['browser_download_url']), None)

    download_url = asset['browser_download_url'] if asset else None

    if not download_url:
        raise CLIError(
            'Could not find extension .whl asset on release {}. '
            'Specify a specific prerelease version with --version '
            'or use latest prerelease with --pre'.format(release['tag_name']))

    extension_name = 'util'
    ext = get_extension(extension_name)
    cur_version = ext.get_version()
    cur_version_str = 'v{}'.format(cur_version)
    if cur_version_str == release['tag_name']:
        logger.warning('There are currently no updates available. %s is the latest version', cur_version_str)
        return
    # Copy current version of extension to tmp directory in case we need to restore it after a failed install.
    backup_dir = os.path.join(tempfile.mkdtemp(), extension_name)
    extension_path = ext.path
    logger.debug('Backing up the current extension: %s to %s', extension_path, backup_dir)
    shutil.copytree(extension_path, backup_dir)
    # Remove current version of the extension
    shutil.rmtree(extension_path)
    # Install newer version
    try:
        _add_whl_ext(cli_ctx=cmd.cli_ctx, source=download_url)
        logger.debug('Deleting backup of old extension at %s', backup_dir)
        shutil.rmtree(backup_dir)
        # This gets the metadata for the extension *after* the update
        _augment_telemetry_with_ext_info(extension_name)
    except Exception as err:
        logger.error('An error occurred whilst updating.')
        logger.error(err)
        logger.debug('Copying %s to %s', backup_dir, extension_path)
        shutil.copytree(backup_dir, extension_path)
        raise CLIError('Failed to update. Rolled {} back to {}.'.format(  # pylint: disable=raise-missing-from
            extension_name, cur_version))
    CommandIndex().invalidate()


def group_delete(cmd, prefix, skip=None):

    client = resource_client_factory(cmd.cli_ctx)
    lock_client = resource_lock_client_factory(cmd.cli_ctx)

    groups = client.resource_groups.list()
    groups = list(groups)

    deleted = []

    for group in [group for group in groups if group.name.startswith(prefix)]:

        if skip and group.name in skip:
            logger.debug('skipping resource group: %s', group.name)
            continue

        locks = lock_client.management_locks.list_at_resource_group_level(group.name)
        locks = list(locks)

        for lock in locks:
            logger.debug('deleting lock: %s', lock.name)
            lock_client.management_locks.delete_at_resource_group_level(group.name, lock.name)

        logger.debug('deleting resource group: %s', group.name)
        client.resource_groups.delete(group.name)

        deleted.append(group)

    return deleted


def keyvault_purge(cmd, skip=None):

    client = keyvault_client_factory(cmd.cli_ctx).vaults

    vaults = client.list_deleted()

    purged = []

    for vault in vaults:

        if skip and vault.name in skip:
            logger.debug('skipping keyvault: %s', vault.name)
            continue

        logger.debug('purging keyvault: %s', vault.name)
        client.begin_purge_deleted(vault.name, vault.properties.location)

        purged.append(vault)

    return purged

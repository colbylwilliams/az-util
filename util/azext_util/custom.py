# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=unused-argument, protected-access, too-many-lines

from knack.log import get_logger
from ._client_factory import resource_client_factory, resource_lock_client_factory

logger = get_logger(__name__)


def group_delete(cmd, prefix, skip=None):

    client = resource_client_factory(cmd.cli_ctx)
    lock_client = resource_lock_client_factory(cmd.cli_ctx)

    groups = client.resource_groups.list()
    groups = list(groups)

    for group in [group for group in groups if group.name.startswith(prefix)]:

        if skip and group.name in skip:
            logger.warning('skipping resource group: %s', group.name)
            continue

        locks = lock_client.management_locks.list_at_resource_group_level(group.name)
        locks = list(locks)

        for lock in locks:
            logger.warning('deleting lock: %s', lock.name)
            lock_client.management_locks.delete_at_resource_group_level(group.name, lock.name)

        logger.warning('deleting resource group: %s', group.name)
        client.resource_groups.delete(group.name)

    return 'done.'

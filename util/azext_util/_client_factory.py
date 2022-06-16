# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.commands.client_factory import get_mgmt_service_client
from azure.cli.core.profiles import ResourceType


def resource_client_factory(cli_ctx, subscription_id=None, **_):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES,
                                   subscription_id=subscription_id)


def resource_lock_client_factory(cli_ctx, subscription_id=None, **_):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_LOCKS,
                                   subscription_id=subscription_id)


def keyvault_client_factory(cli_ctx, subscription_id=None, **_):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_KEYVAULT,
                                   subscription_id=subscription_id)

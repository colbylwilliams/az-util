# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.commands.client_factory import get_mgmt_service_client
from azure.cli.core.profiles import ResourceType


def storage_client_factory(cli_ctx, **_):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_STORAGE)


def web_client_factory(cli_ctx, **_):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_APPSERVICE)


def resource_client_factory(cli_ctx, **_):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES)


def resource_lock_client_factory(cli_ctx, **_):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_LOCKS)


def keyvault_client_factory(cli_ctx, **_):
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_KEYVAULT)

# def cosmosdb_client_factory(cli_ctx, **_):
#     from azure.mgmt.cosmosdb import CosmosDBManagementClient
#     return get_mgmt_service_client(cli_ctx, CosmosDBManagementClient)

# def appconfig_client_factory(cli_ctx, **_):
#     from azure.mgmt.appconfiguration import AppConfigurationManagementClient
#     return get_mgmt_service_client(cli_ctx, AppConfigurationManagementClient)

# def network_client_factory(cli_ctx, **_):
    # return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_NETWORK)

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import requests
from knack.util import CLIError
# from knack.log import get_logger
from azure.cli.core.util import should_disable_connection_verify


def get_github_release(repo='az-util', org='colbylwilliams', version=None, prerelease=False):

    if version and prerelease:
        raise CLIError(
            'usage error: can only use one of --version/-v | --pre')

    url = 'https://api.github.com/repos/{}/{}/releases'.format(org, repo)

    if prerelease:
        version_res = requests.get(url, verify=not should_disable_connection_verify())
        version_json = version_res.json()

        version_prerelease = next((v for v in version_json if v['prerelease']), None)
        if not version_prerelease:
            raise CLIError('--pre no prerelease versions found for {}/{}'.format(org, repo))

        return version_prerelease

    url += ('/tags/{}'.format(version) if version else '/latest')

    version_res = requests.get(url, verify=not should_disable_connection_verify())

    if version_res.status_code == 404:
        raise CLIError(
            'No release version exists for {}/{}. '
            'Specify a specific prerelease version with --version '
            'or use latest prerelease with --pre'.format(org, repo))

    return version_res.json()


def github_release_version_exists(version, repo='az-util', org='colbylwilliams'):

    version_url = 'https://api.github.com/repos/{}/{}/releases/tags/{}'.format(org, repo, version)
    version_res = requests.get(version_url, verify=not should_disable_connection_verify())

    return version_res.status_code < 400

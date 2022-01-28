# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from collections import OrderedDict
from knack.log import get_logger

logger = get_logger(__name__)


def transform_rg_table(result):
    if not isinstance(result, list):
        result = [result]

    output = []

    for r in result:
        output.append(OrderedDict([
            ('Name', r['name']),
            ('Location', r['location']),
            ('Resource ID', r['id']),
        ]))

    return output

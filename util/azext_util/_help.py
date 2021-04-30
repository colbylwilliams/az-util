# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps  # pylint: disable=unused-import

# ----------------
# Util
# ----------------

helps['util'] = """
type: group
short-summary: Utilities for common or tedius tasks.
"""

helps['util group'] = """
type: group
short-summary: Utilities for managing resource groups.
"""

helps['util group delete'] = """
type: command
short-summary: Delete multiple resource groups by name.
examples:
  - name: Delete all resource groups with names starting with test.
    text: az util group delete --prefix test
  - name: Delete all resource groups with names starting with test skipping test123.
    text: az util group delete --prefix test --skip test123
"""

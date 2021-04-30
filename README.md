# az-util

Microsoft Azure CLI Utility 'util' Extension adds useful "utilities" for common or tedious tasks.

## Install

To install the Azure CLI Utility extension, simply run the following command:

```sh
az extension add --source https://github.com/colbylwilliams/az-util/releases/download/v0.1.0/util-0.1.0-py2.py3-none-any.whl -y
```

### Update

To update Azure CLI Utility extension to the latest version:

```sh
az util update
```

or for the latest pre-release version:

```sh
az util update --pre
```

## Commands

This extension adds the following commands.  Use `az util -h` for more information.

---

### util group

Utilities for managing resource groups.

#### util group delete

Delete multiple resource groups by name.

##### examples

Delete all resource groups with names starting with test.

```sh
az util group delete --prefix test
```

Delete all resource groups with names starting with test skipping test123.

```sh
az util group delete --prefix test --skip test123
```

---

### util keyvault

Utilities for managing keyvaults.

#### util keyvault purge

Purge (permanently delete) deleted keyvaults.

##### examples

Purge (permanently delete) all deleted keyvaults.

```sh
az util keyvault purge
```

Purge (permanently delete) all deleted keyvaults skipping test123.

```sh
az util keyvault purge --skip test123
```

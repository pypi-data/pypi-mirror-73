TokkoCLI
---
> Komm her, bleib hier, Wir sind gut zu dir!

**TOC**
+ [Install](#how-to-install-tokko-cli)
+ [Getting Started](#getting-started-with-tokkocli)
    - [Auth](#auth-tools)
    - [User](#user)
        * [Init](#initialize-user-account)
    - [Daemon](#daemon-tools)
        * [Install](#install)
        * [run](#run)
        * [uninstall](#uninstall)
        * [status](#status)
            * [SystemCtl](#systemctl-cli)
    - [RPC](#rpc)
        * [London calling](#call-rpc-functions)
    - [Workflow](#workflow)
        * [First Day](#firstday)
        * [Last Day](#lastday)


# How to install tokko-cli?
```bash
# Using PIP:
sudo -H pip3 install tools/tokko-cli
# Or using setup script:
sudo -H python3 tools/tokko-cli/setup.py install
```

# Getting started with TokkoCLI

## User

User account tools

### Initialize User account

```bash
tokky user init
```

## Auth tools
TokkoAuth lib integrations.

    Not implemented yet!

## Daemon tools

### Install
Install tokkoCLI daemon as SystemD service.
```
$ sudo tokky daemon install
```

### Run
Run attached TokkoCLI Daemon.
```
$ tokky daemon run [--port {custom-port}]
```

### Status
Get current daemon status.
```
$ tokky daemon status
```

#### SystemCtl CLI
Tokko CLI daemon is a SystemD service, therefore common SystemCtl commands are enabled

```
# Check serivce status
systemctl status tokko-cli-daemon.service

# Enable TokkoCLI Daemon serivce
systemctl Enable tokko-cli-daemon.service

# Start TokkoCLI Daemon serivce
systemctl start tokko-cli-daemon.service

# Stop TokkoCLI Daemon serivce
systemctl stop tokko-cli-daemon.service
```

### Uninstall
Remove tokkoCLI daemon from SystemCtl.

```
$ tokky daemon uninstall
```

## RPC
TokkoRPC shell.

### Call rpc functions

```bash
tokky rpc call {function} [--service {my-serice: String}] [--data {data: String}]
```
__Example__
```
$ tokky rpc call echo --data "Hello world!"
>>> "Hello world!"
```

## Workflow


---


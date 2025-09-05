# HCC2 Sample Python Application Template
----

| Version                               | Date       | Note                                                                             |
|---------------------------------------|:----------:|:---------------------------------------------------------------------------------|
| [Revision v1.1](##revision-v11)       | 2024-09-06 | Data point classes generated from TAR.GZ. Improved server ping, main task loop.
| [Revision v1.0](##revision-v10)       | 2024-09-04 | Initial template

---
## Revision v1.1

> ***New Features***
>> - Added AppConfigFile wrapper class which loads in the provided static `TAR.GZ` file
>> - AppConfFile class parses `TAR.GZ` and generates `GeneralDataPoint` and `ConfigDataPoint` classes for use in main.
>
> ***Enhancement / Changes***
>> - Tasks in main are now threaded instead of async. Removes complexity and need for yielding etc.
>> - Provisioning thread prints the current post valid config after a HCC2 deployment.
>> - Improved Rest Server IP resolution, after failed attempts to reach rest server application will restart.
>
> ***Bugs / Issues*** 
>

---
## Revision v1.0

> ***New Features***
>> - **Initial Features**
>>> - Provisioning thread which handles HCC2 deployments. Put new config data into thread safe PostValidConfig class.
>>> - Main async task loop. Contains a empty main and working heartbeat task.
>>> - Subscription service which create working subscription app recieving subscription HCC2 message data.
>
> ***Enhancement / Changes***
>
> ***Bugs / Issues*** 
>> Occasionally the script will fail to resolve the hccRestServer_0 containers IP on edgenet. This will halt the script.
>> On bootup and container reset some lengthly http connection errors may dump in logs.
>

#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "a9d25d58-0d00-4c8f-a1d8-fdb9a364183a")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "4cec91e0-12d2-4fe8-a07a-0eef70ae2c59")
    APP_TYPE = os.environ.get("MicrosoftAppType", "MultiTenant")
    APP_TENANTID = os.environ.get("MicrosoftAppTenantId", "d97de02a-4882-4368-af5b-39b68295eeea")

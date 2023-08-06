# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in project root for information.
# ---------------------------------------------------------

"""Contains functionality to collect model data (e.g. inputs, predictions etc.) in Azure Machine Learning deployments.

The :class:`azureml.monitoring.ModelDataCollector` class enables you to collect model data to a workspace's default
blob storage.
"""
from .modeldatacollector import *

# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.paging import Paged


class PolicyAssignmentPaged(Paged):
    """
    A paging container for iterating over a list of :class:`PolicyAssignment <azure.mgmt.resource.policy.v2018_03_01.models.PolicyAssignment>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[PolicyAssignment]'}
    }

    def __init__(self, *args, **kwargs):

        super(PolicyAssignmentPaged, self).__init__(*args, **kwargs)
class PolicyDefinitionPaged(Paged):
    """
    A paging container for iterating over a list of :class:`PolicyDefinition <azure.mgmt.resource.policy.v2018_03_01.models.PolicyDefinition>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[PolicyDefinition]'}
    }

    def __init__(self, *args, **kwargs):

        super(PolicyDefinitionPaged, self).__init__(*args, **kwargs)
class PolicySetDefinitionPaged(Paged):
    """
    A paging container for iterating over a list of :class:`PolicySetDefinition <azure.mgmt.resource.policy.v2018_03_01.models.PolicySetDefinition>` object
    """

    _attribute_map = {
        'next_link': {'key': 'nextLink', 'type': 'str'},
        'current_page': {'key': 'value', 'type': '[PolicySetDefinition]'}
    }

    def __init__(self, *args, **kwargs):

        super(PolicySetDefinitionPaged, self).__init__(*args, **kwargs)

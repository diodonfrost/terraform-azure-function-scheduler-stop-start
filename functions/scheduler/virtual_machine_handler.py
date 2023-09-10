"""Virtual machine handler module."""

import logging

import azure.mgmt.compute
from azure.identity import DefaultAzureCredential

from .filter_resources_by_tags import FilterByTags


class VirtualMachineScheduler:
    """Abstract virtual machine scheduler in a class."""

    def __init__(self, subscription_id: str) -> None:
        """Initialize Azure client."""
        self.compute_client = azure.mgmt.compute.ComputeManagementClient(
            credential=DefaultAzureCredential(), subscription_id=subscription_id
        )
        self.tag_filter = FilterByTags(subscription_id)

    def stop(self, azure_tags: dict) -> None:
        """Azure virtual machine stop function.

        Stop virtual machines with defined tags.

        :param str azure_tags:
            The key of the tag that you want to filter by.
            For example: {"key": "value"}
        """
        resource_type = "Microsoft.Compute/virtualMachines"
        for vm_id in self.tag_filter.get_resources(azure_tags, resource_type):
            self.compute_client.virtual_machines.begin_deallocate(
                resource_group_name=vm_id.split("/")[4],
                vm_name=vm_id.split("/")[-1],
            )
            logging.info("Stop virtual machine: %s", vm_id)

    def start(self, azure_tags: dict) -> None:
        """Azure virtual machine start function.

        Start virtual machines with defined tags.

        :param str azure_tags:
            The key of the tag that you want to filter by.
            For example: {"key": "value"}
        """
        resource_type = "Microsoft.Compute/virtualMachines"
        for vm_id in self.tag_filter.get_resources(azure_tags, resource_type):
            self.compute_client.virtual_machines.begin_start(
                resource_group_name=vm_id.split("/")[4],
                vm_name=vm_id.split("/")[-1],
            )
            logging.info("Start virtual machine: %s", vm_id)
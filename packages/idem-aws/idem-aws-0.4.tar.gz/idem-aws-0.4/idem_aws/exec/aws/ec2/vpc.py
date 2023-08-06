# -*- coding: utf-8 -*-
"""
EC2 VPC
"""

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    return await hub.aws.client.request(ctx, client="ec2", func="describe_vpcs")


async def create(hub, ctx, name: str, cidr_block: str, **kwargs):
    status, ret = await hub.aws.client.request(
        ctx, client="ec2", func="create_vpc", cidr_block=cidr_block, **kwargs,
    )
    if not status:
        return status, ret
    await hub.aws.resource.tag(
        ctx,
        resource="ec2",
        resource_type="Vpc",
        resource_id=ret["vpc"]["vpc_id"],
        name=name,
    )
    return status, ret


async def delete(hub, ctx, vpc_id: str, **kwargs):
    return await hub.aws.client.request(
        ctx, client="ec2", func="delete_vpc", vpc_id=vpc_id, **kwargs
    )

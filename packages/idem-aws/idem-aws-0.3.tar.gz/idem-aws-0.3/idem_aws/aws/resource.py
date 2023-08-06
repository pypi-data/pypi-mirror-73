__func_alias__ = {"list_": "list"}


async def get(hub, ctx, resource: str):
    """
    Get a boto3 resource and inject the endpoint url
    Handle asynchronous calls
    """
    service = ctx["acct"].session.resource(
        resource, endpoint_url=ctx["acct"].get("endpoint_url")
    )
    if hasattr(service, "__aenter__"):
        async with service as s:
            return s
    else:
        return service


async def tag(hub, ctx, resource: str, resource_type: str, resource_id: str, name: str):
    """
    Tag a resource with the given name and the key specified by the provider
    :param resource:  The name of the resource to fetch (I.E. ec2)
    :param resource_type: The resource function to call on the resource (I.E. Vpc)
    :param resource_id: The ID of the resource to tag
    :param name: The name to apply to the resource with the key specified by the provider
    """
    resource = await hub.aws.resource.get(ctx, resource)
    resource_class = await hub.aws.call.async_wrap(
        getattr(resource, resource_type), resource_id
    )
    return await hub.aws.call.async_wrap(
        resource_class.create_tags, Tags=[{"Key": ctx["acct"].name_tag, "Value": name}]
    )


async def list_(hub, ctx, resource: str):
    service = await hub.aws.client.get(ctx, resource)
    return await hub.aws.call.async_wrap(service.describe_tags)

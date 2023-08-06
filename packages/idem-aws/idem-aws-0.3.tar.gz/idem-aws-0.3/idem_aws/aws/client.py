async def get(hub, ctx, client: str):
    """
    Get a boto3 client and inject the endpoint url
    """
    service = ctx["acct"].session.client(
        client, endpoint_url=ctx["acct"].get("endpoint_url")
    )
    if hasattr(service, "__aenter__"):
        async with service as s:
            return s
    else:
        return service


async def request(hub, ctx, client: str, func: str, *args, **kwargs):
    """
    Make the request for the aws resource.
    Some backends are async and some are not, work them all out here
    """
    service = await hub.aws.client.get(ctx, client)
    return await hub.aws.call.async_wrap(getattr(service, func), *args, **kwargs)

from dict_tools import data


async def pre_get(hub, ctx):
    kwargs = ctx.get_arguments()
    func_ctx = kwargs["ctx"]
    if not func_ctx.get("acct"):
        raise ConnectionError("missing acct profile")
    elif not func_ctx["acct"].get("session"):
        raise ConnectionError("Incomplete profile information: missing session")


async def post_list(hub, ctx):
    ret = data.NamespaceDict()
    for resource in ctx.ret["Tags"]:
        resource_type = resource["ResourceType"]
        if resource_type not in ret:
            ret[resource_type] = data.NamespaceDict()

        resource_id = resource["ResourceId"]
        if resource_id not in ret[resource_type]:
            ret[resource_type][resource_id] = data.NamespaceDict()

        ret[resource_type][resource_id][resource["Key"]] = resource["Value"]
    return ret


async def pre_tag(hub, ctx):
    """
    # Check that a resource doesn't exist with the same tag
    # if it does, raise an error
    """
    kwargs = ctx.get_arguments()
    name = kwargs["name"]
    name_tag = kwargs["ctx"]["acct"].name_tag
    resource_id = kwargs["resource_id"]
    resource_type = kwargs["resource_type"].lower()
    resources = await hub.aws.resource.list(kwargs["ctx"], kwargs["resource"])
    if any(name == tags.get(name_tag) for tags in resources[resource_type].values()):
        raise NameError(
            f"Cannot tag {resource_id}, a {resource_type} with the Tag '{name_tag}:{name}' already exists"
        )


async def call_tag(hub, ctx):
    try:
        return await ctx.func(*ctx.args, **ctx.kwargs)
    except Exception as e:
        return data.NamespaceDict({"exception": str(e), "http_status_code": None})


async def post_tag(hub, ctx):
    # We only tag one thing at a time so there will only be one item in the ret list
    return ctx.ret[0]

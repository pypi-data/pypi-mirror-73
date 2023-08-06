from dict_tools import data


async def pre_get(hub, ctx):
    kwargs = ctx.get_arguments()
    func_ctx = kwargs["ctx"]
    if not func_ctx.get("acct"):
        raise ConnectionError("missing acct profile")
    elif not func_ctx["acct"].get("session"):
        raise ConnectionError("Incomplete profile information: missing session")


def pre_request(hub, ctx):
    """
    Verify that the ctx has all the information it needs from the profile
    """
    kwargs = ctx.get_arguments()
    func_ctx = kwargs["ctx"]
    if not func_ctx.get("acct"):
        raise ConnectionError("missing acct profile")
    elif not func_ctx["acct"].get("session"):
        raise ConnectionError("Incomplete profile information: missing session")


async def call_request(hub, ctx):
    kwargs = ctx.get_arguments()
    try:
        return await ctx.func(
            hub,
            kwargs["ctx"],
            client=kwargs["client"],
            func=kwargs["func"],
            **hub.aws.dict.camelize(kwargs["kwargs"]),
        )
    except Exception as e:
        return data.NamespaceDict({"exception": str(e), "http_status_code": None})


def post_request(hub, ctx):
    ret = ctx.ret
    if isinstance(ret, dict):
        # TODO Put this behind a command line switch and only do it when printing?
        ret = hub.aws.dict.de_camelize(ret)
        ret = hub.aws.dict.flatten_tags(ret)
        response = ret.pop("response_metadata", {})
        return response.get("http_status_code", None) == 200, ret
    return None, ret

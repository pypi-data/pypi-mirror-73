from dict_tools import data


def call_get(hub, ctx):
    new_ctx = data.NamespaceDict()

    # These are extra provider details that won't be passed to the session creation
    new_ctx.name_tag = ctx.kwargs.pop("name_tag", "Name")
    new_ctx.endpoint_url = ctx.kwargs.get("endpoint_url", None)

    kwargs = ctx.get_arguments()
    new_ctx.session = ctx.func(
        hub,
        aws_access_key_id=kwargs.get("aws_access_key_id", kwargs.get("id")),
        aws_secret_access_key=kwargs.get("aws_secret_access_key", kwargs.get("key")),
        aws_session_token=kwargs.get("aws_session_token", kwargs.get("token")),
        region_name=kwargs.get(
            "region_name", kwargs.get("region", kwargs.get("location"))
        ),
        profile_name=kwargs.get("profile_name", kwargs.get("profile")),
    )
    return new_ctx

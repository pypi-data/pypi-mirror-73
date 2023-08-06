from typing import Any, Dict


def sig(hub, ctx, **kwargs) -> Dict[str, Dict[str, Any]]:
    pass


# TODO this needs to be a global contract for exec
def call(hub, ctx):
    func_ctx = ctx.kwargs.get("ctx")
    if func_ctx:
        if not func_ctx.get("acct"):
            raise ValueError("missing account information")
        elif not func_ctx["acct"].get("session"):
            raise ValueError("Incomplete account information: missing api_key")

    return ctx.func(*ctx.args, **ctx.kwargs)


# TODO this needs to be a global contract for exec
def post(hub, ctx):
    """
    If an exec module is run by itself then simply return the result.
    If a state runs it, then return whether or not the exec run was a success
    """
    func_ctx = ctx.args[1]
    status, result = ctx.ret

    if "run_name" in func_ctx:
        # If this is a state run then return the status of the call, otherwise, just return data
        return status, result
    else:
        # If this was just an exec module then ignore the status
        return result

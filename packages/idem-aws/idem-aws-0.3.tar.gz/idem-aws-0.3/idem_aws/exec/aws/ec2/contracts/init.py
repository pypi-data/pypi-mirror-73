from dict_tools import data
from typing import Any, Dict, Tuple


# TODO should this be a top level contract for the entire module as well?
async def post_list(hub, ctx) -> Tuple[bool, Dict[str, Any]]:
    """
    Turn the output of list functions into a dictionary
    """
    func_ctx = ctx.args[1]
    status, result = ctx.ret
    if len(result) > 1:
        return status, result

    items: list = tuple(result.values())[0]

    # Re-arrange the list so that the keys come from the name tag
    ret = data.NamespaceDict()
    for item in items:
        name = item.tags.get(func_ctx["acct"].name_tag)
        if not name:
            hub.log.debug("Ignoring")
        else:
            if name in ret:
                hub.log.error(f"Duplicate Name tags detected: {name}")
                # Come up with an alternate name for listing the duplicate
                j = 1
                new_name = f"{name} ({j})"
                while new_name in ret:
                    j += 1
                    new_name = f"{name} ({j})"
                ret[new_name] = item
            else:
                ret[name] = item

    # TODO is this how filters are meant to be applied?
    # Filter out data based on filters from OPT
    # don't filter if a state is asking
    if hub.OPT.idem.filter and "run_name" not in func_ctx:
        new_ret = data.NamespaceDict()
        for key, value in ret.items():
            new_ret[key] = data.NamespaceDict()
            for k, v in value.items():
                if k in hub.OPT.idem.filter:
                    new_ret[key][k] = v
        ret = new_ret
    return status, ret


# TODO delete this once the recursive contract from the top level applies
def post(hub, ctx):
    """
    in every function, only return the status if a state is asking
    """
    func_ctx = ctx.args[1]
    if "run_name" in func_ctx:
        # If this is a state run then return the status of the call, otherwise, just return data
        return ctx.ret
    else:
        # If this was just an exec module then ignore the status
        return ctx.ret[1]

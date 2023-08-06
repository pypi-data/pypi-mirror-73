from dict_tools import differ
from typing import Any, Dict


async def absent(hub, ctx, name: str, **kwargs) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    ret["result"], vpc_list = await hub.exec.aws.ec2.vpc.list(ctx)
    if not ret["result"]:
        ret["comment"] = vpc_list.get("exception")
        return ret

    changes_old = vpc_list.get(name)

    if not changes_old:
        ret["comment"] = f"AWS vpc {name} is already absent"
        return ret

    status, result = await hub.exec.aws.ec2.vpc.delete(
        ctx, vpc_id=changes_old.vpc_id, **kwargs
    )
    ret["result"] = status
    if not status:
        ret["comment"] = result.get("exception")
        return ret

    ret["comment"] = f"VPC '{name}' was deleted"
    changes_new = result
    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret


async def present(hub, ctx, name: str, cidr_block: str, **kwargs) -> Dict[str, Any]:
    ret = {
        "name": name,
        "result": True,
        "changes": None,
        "comment": "",
    }

    ret["result"], vpc_list = await hub.exec.aws.ec2.vpc.list(ctx)

    if not ret["result"]:
        ret["comment"] = vpc_list.get("exception")
        return ret

    changes_old = vpc_list.get(name)

    if changes_old:
        ret["comment"] = f"AWS vpc {name} is already present"
        return ret

    status, result = await hub.exec.aws.ec2.vpc.create(
        ctx, name=name, cidr_block=cidr_block, **kwargs
    )
    ret["result"] = status
    if not status:
        ret["comment"] = result.get("exception")
        return ret

    ret["comment"] = f"VPC '{name}' was created with VpcId: {result.vpc.vpc_id}"
    changes_new = (await hub.exec.aws.ec2.vpc.list(ctx))[1].get(name)
    ret["changes"] = differ.deep_diff(changes_old, changes_new)

    return ret

# -*- coding: utf-8 -*-
"""
EC2 Volumes (EBS)
"""

# Import third party libs
import botocore.exceptions

__func_alias__ = {"list_": "list"}


async def _volume_description(vol_resource):
    """Make a volume resource type into a more digestable (by idem)
    resource by creating a dictionary that doesn't have callable or
    dunder attributes
    """
    desc = {
        f: getattr(vol_resource, f)
        for f in dir(vol_resource)
        if (not f.startswith("__") and not callable(getattr(vol_resource, f)))
    }
    return desc


async def list_(hub, ctx, **kwargs):
    """describe-volumes

    A quick tool to demonstrate listing volumes

    Filters, per
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.ServiceResource.volumes
    can be passed in.

    The only useful parameter right now is the 'profile' which must be
    a properly configured profile that contains e.g. the region, the
    access key, and the secret key (or which otherwise is configured
    to work already)

    be_verbose: boolean that can be set to expand the info about each volume object

    Test case for using a filter (the ctx isn't being used implicitly in this exec test, but will be later):

    idem exec --acct-profile=<acct profile name> aws.ec2.volume.list be_verbose=True filters='[{"Name": "tag:Name", "Values": ["<the tag you want to match>"]}
    """
    ec2_res = ctx["acct"]["session"].resource("ec2")
    return ec2_res.volumes.filter(**kwargs)


async def get(hub, ctx, volume_id):
    """
    Quick example of returning info about a volume based on passing in its
    ec2 volume ID.

    if "session" is passed via the kwargs, that already created session will
    be used to connect to the ec2 api.

    To narrow down by tag, use the list function.
    """
    ec2_res = ctx["acct"]["session"].resource("ec2")

    vol = ec2_res.Volume(volume_id)
    return await _volume_description(vol)


async def create(
    hub,
    ctx,
    availability_zone,
    name=None,
    size=None,  # not needed if snapshot_id is present
    snapshot_id=None,
    encrypted=False,
    kms_key_id=None,
    volume_type="gp2",
    **kwargs,
):
    """Create a volume using the creating syntax per the arguments
    described at:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_volume

    One minor usability improvement is that since we know we're
    creating a volume, instead of having to pass in a
    TagSpecifications with a ResourceType and a Tags specified, you
    can just specify Tags
    """
    # TODO argument sanitization needs to happen in a contract
    camelize_me = {
        "availability_zone": availability_zone,
        "size": size,
        "snapshot_id": snapshot_id,
        "encrypted": encrypted,
        "kms_key_id": kms_key_id,
        "volume_type": volume_type,
    }
    camelize_me.update(kwargs)
    if "tags" in camelize_me:
        camelize_me["tag_specifications"] = [
            {"ResourceType": "volume", "Tags": kwargs["tags"]}
        ]
        del camelize_me["tags"]
        # Set the name tag, since volumes don't have names otherwise
        if name:
            name_tag = {"Key": "Name", "Value": name}
            camelize_me["tag_specifications"][0]["Tags"].append(name_tag)
    elif name:  # No tags, but we have a name tag to create
        name_tag = {"Key": "Name", "Value": name}
        camelize_me["tag_specifications"] = [
            {"ResourceType": "volume", "Tags": [name_tag]}
        ]

    camelized = hub.aws.dict.camelize(camelize_me)
    # Creating a volume requires the low-level client
    ec2_client = ctx["acct"]["session"].client("ec2")
    hub.log.warning("Going to create a volume")
    try:
        new_volume = ec2_client.create_volume(**camelized)
        hub.log.debug(f"created new volume {new_volume}")
        return_fields = (
            "AvailabilityZone",
            "Encrypted",
            "Size",
            "SnapshotId",
            "State",
            "VolumeId",
            "Iops",
            "Tags",
            "VolumeType",
            "MultiAttachEnabled",
        )

        return [{k: v for k, v in new_volume.items() if k in return_fields}]
    except botocore.exceptions.ClientError as ce:
        hub.log.error(f"Couldn't create the volume because: {str(ce)}")
        return ce


async def destroy(hub, ctx, id_, **kwargs):
    """Destroy an ec2 volume"""
    ec2_res = ctx["acct"]["session"].resource("ec2")
    result = ec2_res.Volume(id_).delete()
    hub.log.debug(f"result is {result}")
    return [result]

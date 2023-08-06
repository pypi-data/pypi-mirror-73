from typing import Any, Dict


async def gather(hub) -> Dict[str, Any]:
    sub_profiles = {}
    for profile, ctx in hub.acct.PROFILES.get("aws.boto", {}).items():
        # Add a boto session to the ctx for exec and state modules
        # Strip any args that were used for authentication
        # Boto uses the default account if none was specified
        sub_profiles[profile] = hub.aws.session.get(**ctx)
    return sub_profiles

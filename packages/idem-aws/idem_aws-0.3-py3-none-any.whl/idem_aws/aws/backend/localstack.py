try:
    from localstack_client import session as localstack

    HAS_LOCALSTACK = True
except ImportError:
    HAS_LOCALSTACK = False


def __virtual__(hub):
    return HAS_LOCALSTACK


def __init__(hub):
    pass


# Stub that will get profile info out of the pop `acct` plugin.
def get(
    hub,
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    aws_session_token: str = None,
    region_name: str = None,
    profile_name: str = None,
) -> localstack.Session:
    return localstack.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name,
        profile_name=profile_name,
        # TODO add the ability to use this based on endpoint_url
        localstack_host=None,
    )

def get(hub, *args, **kwargs):
    default = "aioboto3"
    backends = hub.aws.backend._loaded.keys()
    # Use the specified session backend
    # if it doesn't exist, fall back on the default if it is loaded
    # if the default isn't loaded then use the first loaded session backend
    session_backend = (
        hub.OPT.idem.session_backend or default
        if default in backends
        else next(iter(backends))
    )
    return getattr(hub.aws.backend, session_backend).get(*args, **kwargs)

class CacheProvider:

    @staticmethod
    def from_cache(responder):
        def wrapped(*args, **kwargs):
            resp = args[2]
            if not resp.context.get('cached'):
                responder(*args, **kwargs)
        return wrapped

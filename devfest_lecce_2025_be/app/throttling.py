from rest_framework.throttling import SimpleRateThrottle


class ScanRateThrottle(SimpleRateThrottle):
    scope = "scan"

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            ident = request.user.uid
        else:
            ident = self.get_ident(request)

        return self.cache_format % {"scope": self.scope, "ident": ident}

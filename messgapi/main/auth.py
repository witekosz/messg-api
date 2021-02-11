from ninja.security import APIKeyHeader

from .models import APIKey


class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        key = APIKey.objects.filter(key=key).first()

        if key:
            return key.key
        else:
            return None


header_key = ApiKey()

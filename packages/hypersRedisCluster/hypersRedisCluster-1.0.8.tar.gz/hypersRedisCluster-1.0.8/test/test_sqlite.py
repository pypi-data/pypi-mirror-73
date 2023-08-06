SECRET_KEY = "django_tests_secret_key"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION" : "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "hypersRedisCluster.client.RedisClusterClient",
        }
    },
}

INSTALLED_APPS = (
    "django.contrib.sessions",
)
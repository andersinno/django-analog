SECRET_KEY = "analog"
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "analog_tests",
)
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

ANALOG_KINDS = {"custom_kind": 3010}

ANALOG_KIND_LABELS = {"custom_kind": "very custom"}

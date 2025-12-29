# DB settings
export DB_ENGINE=""
export DB_NAME=""
export DB_USER=""
export DB_PASSWORD=""
export DB_HOST=""
export DB_PORT=""

# Secret Key
export SECRET_KEY=""
# Debug mode
export DEBUG="True"
# Allowed hosts
export ALLOWED_HOSTS="host1,host2,..."
export CSRF_TRUSTED_ORIGINS="http://127.0.0.1,http://localhost,https://host1,..."

# Email settings
#export EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"
export EMAIL_BACKEND=""
export EMAIL_USE_TLS="False"
export EMAIL_USE_SSL="False"
export DEFAULT_FROM_EMAIL=""
export EMAIL_HOST=""
export EMAIL_HOST_USER=""
export EMAIL_HOST_PASSWORD=""
export EMAIL_PORT=""

# PayPal
export PAYPAL_TEST="True"
export PAYPAL_RECEIVER_EMAIL="" # Business Sandbox account
daphne config.asgi:application -b 0.0.0.0 -p $PORT # \
  # & celery -A config worker -E -l info \
  # & celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
#!/bin/sh

echo DEBUG=0 >> .env.prod
echo SQL_ENGINE=django.db.backends.postgresql >> .env.prod
echo DATABASE=postgres >> .env.prod

echo SECRET_KEY=$SECRET_KEY >> .env.prod
echo SQL_DATABASE=$SQL_DATABASE >> .env.prod
echo SQL_USER=$SQL_USER >> .env.prod
echo SQL_PASSWORD=$SQL_PASSWORD >> .env.prod
echo SQL_HOST=$SQL_HOST >> .env.prod
echo SQL_PORT=$SQL_PORT >> .env.prod
echo SQL_SSL=$SQL_SSL >> .env.prod

echo DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS >> .env.prod
echo STRAVA_CLIENT_ID=$STRAVA_CLIENT_ID >> .env.prod
echo STRAVA_CLIENT_SECRET=$STRAVA_CLIENT_SECRET>> .env.prod
echo CORS_RULE=$CORS_RULE >> .env.prod
echo SIG_KEY=$SIG_KEY >> .env.prod
echo JWT_SECRET=$JWT_SECRET >> .env.prod

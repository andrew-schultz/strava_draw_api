#!/bin/sh

# ssh -o StrictHostKeyChecking=no root@$DIGITAL_OCEAN_IP_ADDRESS << 'ENDSSH'
#   cd /app
#   export $(cat .env.prod | xargs)
#   docker login -u $CI_REGISTRY_USER -p $CI_JOB_TOKEN $CI_REGISTRY
#   docker pull $IMAGE:web
#   docker pull $IMAGE:nginx
#   docker pull $IMAGE:certbot
#   docker compose -f docker-compose.yml up -d
# ENDSSH

ssh -o StrictHostKeyChecking=no root@$DIGITAL_OCEAN_IP_ADDRESS << 'ENDSSH'
  cd /app
  export $(cat .env.prod | xargs)
  docker login -u $CI_REGISTRY_USER -p $CI_JOB_TOKEN $CI_REGISTRY
  docker pull $IMAGE:web
  docker pull $IMAGE:nginx
  docker pull $IMAGE:certbot
ENDSSH
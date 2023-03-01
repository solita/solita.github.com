#!/bin/sh

CONTAINER_NAME=solita-dev-blog-tag-remover
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"


pwd
if [ ! "$(docker ps -a | grep $CONTAINER_NAME)" ]
then
  docker build -t $CONTAINER_NAME $SCRIPTPATH -f $SCRIPTPATH/Dockerfile-tag-cleaner
fi

docker run \
-v ${SCRIPTPATH}/tag-cleaner.py:/usr/src/app/tag-cleaner.py \
-v ${SCRIPTPATH}/../_posts:/usr/src/app/_posts \
$CONTAINER_NAME
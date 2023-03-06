#!/bin/sh

CONTAINER_NAME=solita-dev-blog-rule-keeper
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

if [ ! "$(docker ps -a | grep $CONTAINER_NAME)" ]
then
  docker build -t $CONTAINER_NAME $SCRIPTPATH -f $SCRIPTPATH/Dockerfile-rule-keeper
fi

docker run \
-v ${SCRIPTPATH}:/usr/src/app \
-v ${SCRIPTPATH}/../_posts:/usr/src/app/_posts $CONTAINER_NAME
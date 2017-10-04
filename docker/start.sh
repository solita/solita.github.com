#!/bin/bash
set -o errexit

stop_old_container () {
    if docker kill solita-blag; then
        docker rm solita-blag
    fi
}

main () {
    stop_old_container
    docker run -it -v `pwd`:/solita-blag --name solita-blag --rm -p 4444:4000 solita-blag
}

main "$@"

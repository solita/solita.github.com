#!/bin/bash
set -o errexit

main() {
    docker run -it -v $(pwd):/solita-blag --name solita-blag --rm -p 4444:4000 solita-blag
}

main "$@"

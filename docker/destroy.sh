#!/bin/bash
set -o errexit

main() {
    docker rmi solita-blag
}

main "$@"

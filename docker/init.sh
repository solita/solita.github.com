#!/bin/bash
set -o errexit

main() {
    docker build -t solita-blag .
}

main "$@"

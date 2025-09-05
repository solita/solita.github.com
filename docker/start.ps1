# start.ps1
$ErrorActionPreference = "Stop"

function Main {
    docker run -it -v "${PWD}:/solita-blag" --name solita-blag --rm -p 4444:4000 solita-blag
}

Main @args

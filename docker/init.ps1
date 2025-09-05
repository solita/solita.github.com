# init.ps1
$ErrorActionPreference = "Stop"

function Main {
    docker build -t solita-blag .
}

Main @args
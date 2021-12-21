---
layout: post
title: Docker on WSL2 without Docker Desktop
author: tepsley
excerpt: >
  After January 31, 2022, Docker Desktop will require a paid subscription. Here you can find instructions for running Docker on WSL2 under Windows without Docker Desktop (target distributions being Debian & Ubuntu).
tags:
  - Software Development
  - Docker
  - Docker Desktop
  - Windows
  - WSL2
  - Debian
  - Ubuntu
---

> <span style="font-size: 13px;">After January 31, 2022, Docker Desktop will require a paid subscription.<br/>Commercial use of Docker Desktop in larger enterprises (more than 250 employees OR more than $10 million USD in annual revenue) requires a Docker Pro, Team or Business subscription for as little as $5 per user per month.<br/>The existing Docker Free subscription has been renamed Docker Personal. Docker Desktop remains free for personal use, education, non-commercial open source projects, and small businesses (fewer than 250 employees AND less than $10M USD in annual revenue).<br/>Source: [https://www.docker.com/legal/docker-subscription-service-agreement](https://www.docker.com/legal/docker-subscription-service-agreement)</span>

## So, how to run Docker on WSL2 under Windows without Docker Desktop (Debian / Ubuntu)?

### Start by removing any old Docker related installations

- On Windows: uninstall Docker Desktop
- On WSL2: `sudo apt remove docker docker-engine docker.io containerd runc`

### Continue on WSL2 with the following

1. Install pre-required packages
   - `sudo apt install --no-install-recommends apt-transport-https ca-certificates curl gnupg2`
2. Configure package repository
   - `source /etc/os-release`
   - `curl -fsSL https://download.docker.com/linux/${ID}/gpg | sudo apt-key add -`
   - `echo "deb [arch=amd64] https://download.docker.com/linux/${ID} ${VERSION_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/docker.list`
   - `sudo apt update`
3. Install `Docker`
   - `sudo apt install docker-ce docker-ce-cli containerd.io`
4. Add user to group
   - `sudo usermod -aG docker $USER`
5. Configure `dockerd`
   - `DOCKER_DIR=/mnt/wsl/shared-docker`
   - `mkdir -pm o=,ug=rwx "$DOCKER_DIR"`
   - `chgrp docker "$DOCKER_DIR"`
   - `sudo mkdir /etc/docker`
   - `sudo <your_text_editor> /etc/docker/daemon.json`<br/><br/>
     <code>
     {<br/>&nbsp;&nbsp;&nbsp;"hosts": ["unix:///mnt/wsl/shared-docker/docker.sock"]<br/>}
     </code><br/><br/>
     - **Note!** `Debian` will also need the additional configuration to the same file
       - `"iptables": false`

### Now you're ready to launch `dockerd` and see if it works

- Run command "`sudo dockerd`" - if the command ends with "`API listen on /mnt/wsl/shared-docker/docker.sock`", things are working
- You can perform an additional test by opening a new terminal and running<br/><br/>
  "`docker -H unix:///mnt/wsl/shared-docker/docker.sock run --rm hello-world`"

### Ok, things are working? Great!

Then it's time to create a launch script for `dockerd`. There are two options, manual & automatic

- To always run `dockerd` automatically
  - Add the following to `.bashrc` or `.profile` (make sure "`DOCKER_DISTRO`" matches your distro, you can check it by running "`wsl -l -q`" in Powershell)<br/><br/>
    <code>
    DOCKER_DISTRO="Ubuntu-20.04"<br/>
    DOCKER_DIR=/mnt/wsl/shared-docker<br/>
    DOCKER_SOCK="$DOCKER_DIR/docker.sock"<br/>
       export DOCKER_HOST="unix://$DOCKER_SOCK"<br/>
    if [ ! -S "$DOCKER_SOCK" ]; then<br/>
    &nbsp;&nbsp;&nbsp;mkdir -pm o=,ug=rwx "$DOCKER_DIR"<br/>
     &nbsp;&nbsp;&nbsp;chgrp docker "$DOCKER_DIR"<br/>
    &nbsp;&nbsp;&nbsp;/mnt/c/Windows/System32/wsl.exe -d $DOCKER_DISTRO sh -c "nohup sudo -b dockerd <code /dev/null > $DOCKER_DIR/dockerd.log 2>&1"<br/>
    fi
    </code>
- To manually run `dockerd`
  - Add the following to your `.bashrc `or `.profile`<br/><br/>
    <code>
    DOCKER_SOCK="/mnt/wsl/shared-docker/docker.sock"<br/>
    test -S "$DOCKER_SOCK" && export DOCKER_HOST="unix://$DOCKER_SOCK"
    </code>

### Want to go passwordless with the launching of `dockerd`?

All you need to do is

- `sudo visudo`
- `%docker ALL=(ALL) NOPASSWD: /usr/bin/dockerd`

### Enable / disable `BuildKit` (optional)

You may end up wanting to enable/disable [BuildKit](https://docs.docker.com/develop/develop-images/build_enhancements/) depending on your use cases (basically to end up with the classic output with `Docker`), and the easiest way for this is to just add the following to your `.bashrc` or `.profile`<br/><br/>
<code>
&nbsp;&nbsp;&nbsp;export DOCKER_BUILDKIT=0<br/>
&nbsp;&nbsp;&nbsp;export BUILDKIT_PROGRESS=plain
</code>

### Adding some finishing touches

To wrap things up, you most likely will want to install `docker-compose`. You can start by checking up the number of the latest stable version from the [Docker Compose documentation](https://docs.docker.com/compose/install/) and doing the following (we'll be using version `1.29.2` in this example)

- `COMPOSE_VERSION=1.29.2`
- `sudo curl -L "https://github.com/docker/compose/releases/download/$COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
- `sudo chmod +x /usr/local/bin/docker-compose`

## Links and references

- [Docker subscription service agreement](https://www.docker.com/legal/docker-subscription-service-agreement)
- [BuildKit](https://docs.docker.com/develop/develop-images/build_enhancements/)
- [Docker Compose](https://docs.docker.com/compose/install/)

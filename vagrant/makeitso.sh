#!/bin/bash
curl -L https://get.rvm.io | bash -s stable  
source /etc/profile.d/rvm.sh
rvm install 1.9.3
rvm use 1.9.3
iptables -F
gem install bundler
gem install rdiscount
gem install jekyll -V
cd /env
jekyll serve --watch

#!/bin/bash
curl -L https://get.rvm.io | bash -s stable  
source /home/vagrant/.rvm/scripts/rvm
rvm install 1.9.3
rvm use 1.9.3
gem install bundler
gem install jekyll
gem install rdiscount
iptables -F
cd /env
jekyll serve --watch

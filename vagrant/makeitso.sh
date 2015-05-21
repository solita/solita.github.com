#!/bin/bash
curl -sSL https://rvm.io/mpapis.asc | sudo gpg2 --import -
curl -L https://get.rvm.io | bash -s stable
source /etc/profile.d/rvm.sh
rvm install 2.2
rvm use 2.2
iptables -F
gem install bundler
cd /env
bundle install
bundle exec foreman start

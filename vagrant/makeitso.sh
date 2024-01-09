#!/bin/bash
curl -sSL https://rvm.io/mpapis.asc | sudo gpg2 --import -
curl -L https://get.rvm.io | bash -s stable
source /etc/profile.d/rvm.sh
rvm install 2.7.3
rvm use 2.7.3
iptables -F
gem install bundler -v 2.4.22
cd /env
bundle install
bundle exec jekyll serve --watch --host 0.0.0.0

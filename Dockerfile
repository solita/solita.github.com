FROM ruby:2.7.4

RUN mkdir /solita-blag
WORKDIR /solita-blag
VOLUME /solita-blag

ENV LANG C.UTF-8

# seems that bundler version has to follow ruby version to work
RUN gem install bundler -v 2.4.22
ADD Gemfile /solita-blag
ADD Gemfile.lock /solita-blag
RUN bundle install

CMD ["bundle", "exec", "jekyll", "serve", "--watch", "--host", "0.0.0.0"]
EXPOSE 4000/tcp

FROM ruby:2.2

RUN mkdir /solita-blag
WORKDIR /solita-blag
VOLUME /solita-blag

ENV LANG C.UTF-8

RUN gem install bundler foreman
ADD Gemfile /solita-blag
ADD Gemfile.lock /solita-blag
RUN bundle install

CMD ["foreman", "start"]

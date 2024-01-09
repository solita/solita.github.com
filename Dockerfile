FROM ruby:2.7.3

RUN mkdir /solita-blag
WORKDIR /solita-blag
VOLUME /solita-blag

ENV LANG C.UTF-8

RUN gem install bundler
ADD Gemfile /solita-blag
ADD Gemfile.lock /solita-blag
RUN bundle install

CMD ["bundle", "exec", "jekyll", "serve", "--watch", "--host", "0.0.0.0"]
EXPOSE 4000/tcp

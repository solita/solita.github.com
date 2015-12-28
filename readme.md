# /dev/solita/greetings

Here are some developer-oriented thoughts from [Solita Oy](http://www.solita.fi/). Our stories have not yet been told. More will come. Stay tuned at <http://dev.solita.fi>.

## Writing

We use a combination of Jekyll and Github Pages to run the site.

If you want to write a post, here's how:

1. Fork this project to yourself (upper right corner)
  - You need a Github account to do this
2. Clone your own fork to your computer (git clone)
3. Add your author info to `_config.yml`
  - The email value is a MD5 hash of your email
4. Write a new post under the `_posts` folder using Markdown, look at other posts for example of what to write there
5. If you have Ruby and Jekyll, preview your post locally (instructions below)
6. Create a pull request at https://github.com/solita/solita.github.com/pull/new/master
  - Choose your fork on the right
  - Write some info about the post
7. Wait for comments and publish!


## Previewing posts

You need Ruby and Jekyll if you want to preview your posts locally on the blog. If you're fine with just previewing the Markdown, you can use a Markdown preview script, like [this one for Sublime Text](https://github.com/revolunet/sublimetext-markdown-preview).


### Option A, Running a virtual machine (standardized environment)

1. Install Vagrant
2. Install Virtualbox
3. `cd vagrant`
4. `vagrant up blag`
5. Wait patiently as the ruby goodness is downloaded and configured
6. http://localhost:4444 now should serve your version of the blog

If anything goes wrong, good luck. vagrant ssh blag and try figure it out.

When you're done you might want to shutdown the virtual machine. vagrant destroy or something like that.


### Option B, Installing Ruby on your workstation

For Windows, download & install the latest Ruby 1.9.x and Development Kit from http://rubyinstaller.org/downloads/  
**Note:** Make sure to tick the checkbox "Add Ruby to PATH" (or something). You can also try: https://github.com/vertiginous/pik/

For OSX(/Linux), use the instructions below. If you have installed Xcode, you might have ruby (1.9.2 or something like that) already. No guarantinees about this working with that so use RVM

1. `curl -L https://get.rvm.io | bash -s stable --ruby=1.9.3`
2. fork this repo
3. go to your working copy of solita.github.com
4. `rvm use 1.9.3`
5. verify that 1.9.3 used by `ruby -v`
(On linux you might need to fix gnome-termina: http://rvm.io/integration/gnome-terminal)
6. `gem install bundler`
7. Run `bundle install` for depencies
8. Make sure the installation succeeds
9. Type in: `bundle exec jekyll serve --watch`
10. Open browser to: http://localhost:4000/

Also seems to be working with Ruby 2.0.0p0/247

## Development

For development, you need Ruby and Jekyll. If you want to tweak the CSS, you need Compass. Also, if you want to make stuff easier, install foreman.

1. Install Ruby (above)
2. Go to your cloned copy of solita.github.com
3. To install Jekyll, Compass and foreman, type into a command prompt or terminal: `bundle install`
4. Make sure the install succeeds
5. Type in: `bundle exec foreman start`
6. Jekyll and Compass should start!

## Technology stack

/dev/solita is built using all the hippiest hip technologies available:

    git, Github Pages, Ruby, Jekyll, Markdown, Sass, Compass, foreman, jQuery, Gravatar, disqus, Google Analytics, AddThis

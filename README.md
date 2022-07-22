# /dev/solita

A blog from developers to developers. Developer-oriented insights from the folks at [Solita](https://www.solita.fi/). Check it out at [dev.solita.fi](https://dev.solita.fi)!

## Writing a blog post

If you want to write a post, here's how:

1. Fork this repository under your own GitHub account
2. Clone your own fork to your local computer
3. Add your author details to `_config.yml`
   - The email value is a MD5 hash of your email
   - Optional: to have your avatar show up, make sure you have a [Gravatar account](https://gravatar.com) registered with your solita.fi email address and a photo of yourself
4. Write a new post under the `_posts` folder using Markdown

   - Name the file with this format: `YYYY-MM-DD-post-name.md`
   - You might want to copy some previous post as a template
   - If you don't see your blog post, change the date on the file to today or a past date
   - Normally the publication date of the post is read from the filename. In this case the publishing time will show up as 00:00:00. If you want to specify the exact time your post was published, you can add a date field to your post's front matter. In the date field you can specify the publication time in the format `YYYY-MM-DD HH:MM:SS +/-TTTT`. For example:

     ```yml
     ---
     title: Post Title
     date: 2016-04-25 13:30:00 +0200
     ....
     ---
     ```

5. Preview and proof read your post. You have three options for previewing:
   - Use your IDE
     - VS Code: Command palette -> Markdown: Open preview
     - IDEA: Just open the file
     - Sublime Text: [MarkdownPreview](https://github.com/facelessuser/MarkdownPreview)
   - Preview the post in GitHub (Pull request -> Files changed -> ... on your post -> View file)
   - [Run the site locally](#running-the-site-locally) and preview the post in it's natural habitat
6. [Submit a pull request](https://github.com/solita/solita.github.com/pull/new/master)
   - Select _compare accross forks_
   - Choose your fork on the right
   - Write an informative description for your pull request
7. Ask someone to review your post
8. Publish by merging the branch

## Running the site locally

### Option A: Running the site in a container (recommended)

1. Install [Docker](https://docker.com) or [Podman](https://podman.io) (with `alias docker=podman`)
2. Run `./docker/init.sh` (need to be run only the first time launching the site)
3. Run `./docker/start.sh`
4. The blog should now be live at [localhost:4444](http://localhost:4444)
5. Stop the container with `ctrl+c`

#### Tips and tricks

- `./docker/destroy.sh` -> Delete image
- `./docker/troubleshoot.sh` -> Open bash to container without starting jekyl and compass

### Option B: Running a Vagrant virtual machine

1. Install Vagrant
2. Install Virtualbox
3. Run `cd vagrant`
4. Run `vagrant up blag`
5. Wait patiently as the ruby goodness is downloaded and configured
6. The blog should now be live at [localhost:4444](http://localhost:4444)

#### Tips and tricks

- If anything goes wrong, good luck. `vagrant ssh blag` and try figure it out.
- When you're done you might want to shutdown the virtual machine. `vagrant destroy` or something like that.

### Option C: Running with local Ruby installation

1. Navigate to your working directory and make sure you are running a comatible version of Ruby with `ruby -v`
2. `gem install bundler`
3. `bundle install`
4. `bundle exec jekyll serve --watch`
5. The blog should now be live at [localhost:4000](http://localhost:4000)

#### Tips and tricks

- It's highly recommended to use a Ruby version manager like [rvm](https://rvm.io) or [rbenv](https://github.com/rbenv/rbenv).
- For maximum compatibility, use the same version of Ruby as [GitHub pages is using](https://pages.github.com/versions/).

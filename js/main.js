(function () {

    var AVATAR_SIZE = 50;

    $(document).ready(function () {
        var avatarTemplate = $('#templates .avatar').detach();

        $('.post-meta').each(function () {
            var $this = $(this),
                authorLink = $this.find('.author a'),
                url = authorLink.attr('href'),
                username = authorLink.text(),
                email = authorLink.attr('title'),
                avatar = avatarTemplate.clone(),

            directives = {
                img: {
                    src: function () { return get_gravatar(email); },
                    alt: function () { return username; }
                }
            };

            avatar.render({}, directives);
            avatar.attr('href', url);
            $this.append(avatar);
        });
    });

    function get_gravatar(email, size) {
        size = size || AVATAR_SIZE;
        return 'http://www.gravatar.com/avatar/' + email + '.jpg';
    }

}());

(function () {

    var AVATAR_SIZE = 80;

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
                        src: function () {
                            return get_gravatar(email);
                        },
                        alt: function () {
                            return username;
                        }
                    }
                };

            avatar.render({}, directives);
            avatar.attr('href', url);
            $this.prepend(avatar);
        });
    });

    function get_gravatar(email, size) {
        size = size || AVATAR_SIZE;
        var defaultImage = 'https://preview.ibb.co/cSmCtH/solita_person_placeholder.png';
        return 'https://www.gravatar.com/avatar/' + email + '.jpg?size=' + size + '&default=' + defaultImage;
    }

}());

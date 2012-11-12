(function () {

    var AVATAR_SIZE = 50;

    $(document).ready(function () {
        var avatarTemplate = $('#templates .avatar').detach();

        $('.post-meta').each(function () {
            var $this = $(this);
            var email = $this.find('.author a').attr('title');
            console.log(email);
            var avatar = avatarTemplate.clone();

            var directives = {
                img: {
                    src: function () { return get_gravatar(email); },
                    alt: function () { return 'alt test'; }
                }
            };

            avatar.render({ href: 'yes' }, directives);

            $this.append(avatar);
        });
    });

    function get_gravatar(email, size) {
        size = size || AVATAR_SIZE;
        return 'http://www.gravatar.com/avatar/' + MD5(email) + '.jpg?s=' + size;
    }

}());

(function () {

    var AVATAR_SIZE = 80;

    $(document).ready(function () {
        var avatarTemplate = $('#templates .avatar').detach();

        var menuToggle = $('#menu-toggle'),
            primaryNav = $('#primary-navigation');
        
        menuToggle.on('click', function(){
            menuToggle.toggleClass('menu-toggle--active');
            primaryNav.css('display', menuToggle.hasClass('menu-toggle--active') ? 'block' : '');
        });

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
            avatar.attr('aria-hidden', true);
            $this.prepend(avatar);
        });
    });

    function get_gravatar(email, size) {
        size = size || AVATAR_SIZE;
        var defaultImage = 'https://dev.solita.fi/img/solita-person-placeholder.png';
        return 'https://www.gravatar.com/avatar/' + email + '.jpg?size=' + size + '&default=' + defaultImage;
    }

}());

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
                imgUrl = get_gravatar(email);

            $this.prepend(`<a href="${url}" class="avatar"><img aria-hidden="true" class="img" src="${imgUrl}" alt="${username}"/></a>`);
        });
    });

    function get_gravatar(email, size) {
        size = size || AVATAR_SIZE;
        var defaultImage = 'https://dev.solita.fi/img/solita-person-placeholder.png';
        return 'https://www.gravatar.com/avatar/' + email + '.jpg?size=' + size + '&default=' + defaultImage;
    }

}());

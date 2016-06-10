var more_success, more_fail;

if (app.DEBUG_DIR) {
    more_success = [
        'https://cdnjs.cloudflare.com/ajax/libs/jquery-migrate/1.2.1/jquery-migrate.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/zclip/1.1.2/jquery.zclip.min.js',
        '/site_media/css/min/theme.min.css',
        '/site_media/css/min/filemanager.min.css'
    ];
    more_fail = [
        '/site_media/js/public/min/core.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/jquery-migrate/1.2.1/jquery-migrate.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/zclip/1.1.2/jquery.zclip.min.js',
        '/site_media/css/min/core.min.css',
        '/site_media/css/min/filemanager.min.css'
    ];
} else {
    more_success = [
        'https://cdnjs.cloudflare.com/ajax/libs/jquery-migrate/1.2.1/jquery-migrate.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/zclip/1.1.2/jquery.zclip.min.js',
        '/site_media/css/theme.css',
        '/site_media/css/palette.css',
        '/site_media/css/_filemanager.css'
    ];
    more_fail = [
        '/site_media/js/jquery.min.js',
        '/site_media/js/bootstrap.min.js',
        '/site_media/css/bootstrap.min.css'
    ].concat(more_success);
}

head.load('https://cdnjs.cloudflare.com/ajax/libs/jquery/' + app.js_ver.jquery + '/jquery.min.js', function() {
    head.test(window.$, [
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/' + app.js_ver.bootstrap + '/css/bootstrap.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/' + app.js_ver.bootstrap + '/js/bootstrap.min.js'
    ].concat(more_success), more_fail, function(flag) {
        app.isCDN = flag;
        $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + '_filemanager' + app.DEBUG_STR + '.js');
    });
});

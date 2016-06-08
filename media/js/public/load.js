var more_success, more_fail;
var d3 = undefined;
app.isCDN = false;
app.isLoaded = false;
app.modPrimerize = {'job_type': undefined, 'job_id': undefined};
app.mod96Plate = {};

if (app.DEBUG_DIR) {
    more_success = ['/site_media/css/min/theme.min.css'];
    more_fail = [
        '/site_media/js/public/min/core.min.js',
        '/site_media/css/min/core.min.css'
    ];
} else {
    more_success = [
        '/site_media/css/theme.css',
        '/site_media/css/palette.css'
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
        $.ajaxSetup({'cache': true});
        $.getScript('/site_media/js/public/' + app.DEBUG_DIR + 'menu' + app.DEBUG_STR + '.js');
        $("head").append('<link rel="shortcut icon" type="image/gif" href="/site_media/images/icon_primerize.png" />');
        $("head").append('<link rel="icon" type="image/gif" href="/site_media/images/icon_primerize.png" />');
    });
});

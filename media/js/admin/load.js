var more_success, more_fail, Suit;

if (app.DEBUG_DIR) {
    more_success = [
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/' + app.js_ver.bootstrap + '/css/bootstrap.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/' + app.js_ver.bootstrap + '/js/bootstrap.min.js',
        '/site_media/js/suit/min/core.min.js',
        '/site_media/js/suit/min/form.min.js',
        '/site_media/css/min/suit.min.css',
        '/site_media/css/min/theme.min.css',
        '/site_media/css/min/admin.min.css'
    ];
    more_fail = [
        '/site_media/js/public/min/core.min.js',
        '/site_media/js/suit/min/core.min.js',
        '/site_media/js/suit/min/form.min.js',
        '/site_media/css/min/suit.min.css',
        '/site_media/css/min/core.min.css'
    ];
} else {
    more_share = [
        '/site_media/js/suit/core.js',
        '/site_media/js/suit/RelatedObjectLookups.js',
        '/site_media/js/suit/jquery.init.js',
        '/site_media/js/suit/jquery.formset.js',
        '/site_media/js/suit/actions.js',
        '/site_media/js/suit/DateTimeShortcuts.js',
        '/site_media/js/suit/calendar.js',
        '/site_media/js/suit/RelatedWidgetWrapper.js',
        '/site_media/js/suit/SelectBox.js',
        '/site_media/js/suit/SelectFilter2.js',
        '/site_media/css/_suit.css',
        '/site_media/css/theme.css',
        '/site_media/css/palette.css',
        '/site_media/css/admin.css'
    ];
    more_success = [
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/' + app.js_ver.bootstrap + '/css/bootstrap.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/' + app.js_ver.bootstrap + '/js/bootstrap.min.js'
    ].concat(more_share);
    more_fail = [
        '/site_media/js/jquery.min.js',
        '/site_media/js/bootstrap.min.js',
        '/site_media/css/bootstrap.min.css'
    ].concat(more_share);
}

head.load('https://cdnjs.cloudflare.com/ajax/libs/jquery/' + app.js_ver.jquery + '/jquery.min.js', function() {
    head.test(window.$, [''], ['/site_media/js/jquery.min.js'], function(flag) {
        Suit = { $: $.noConflict() }; if (!$) $ = Suit.$;
        app.isCDN = flag;
        $("head").append('<link rel="shortcut icon" type="image/gif" href="/site_media/images/icon_primerize.png" />');
        $("head").append('<link rel="icon" type="image/gif" href="/site_media/images/icon_primerize.png" />');

        head.load(app.isCDN ? more_success : more_fail, function() {
            $.ajaxSetup({'cache': true});
            if (!app.DEBUG_DIR) {
                $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + '_suit' + app.DEBUG_STR + '.js');
                $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + 'clock' + app.DEBUG_STR + '.js');
            }
            $.getScript('/site_media/js/admin/' + app.DEBUG_DIR + 'menu' + app.DEBUG_STR + '.js');

            google.charts.load('visualization', '1', {packages: ['corechart', 'calendar', 'map']});

        });
    });
});

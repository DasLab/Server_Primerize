from django.conf.urls import include, url, handler400, handler403, handler404, handler500
from django.contrib import admin
from django.views.generic import RedirectView
from django.views.static import serve

from adminplus.sites import AdminSitePlus
from filemanager import path_end

from src.settings import MEDIA_ROOT, DEBUG, IS_MAINTENANCE, env
from src import user
from src import views
from src import wrapper_1d, wrapper_2d

admin.site = AdminSitePlus()
admin.site.index_title = '%s Administration' % env('SERVER_NAME')
admin.autodiscover()
admin.site.login = user.user_login
admin.site.logout = user.user_logout


if IS_MAINTENANCE:
    urlpatterns = [
        url(r'^ping_test/?$', views.ping_test),
        url(r'^get_admin/?$', views.get_admin),
        url(r'^get_js/?$', views.get_js),

        url(r'^site_media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT + '/media'}),
        url(r'^robots.txt$', serve, kwargs={'path': 'robots.txt', 'document_root': MEDIA_ROOT}),

        url(r'^$', views.error503),
        url(r'^.*/?$', RedirectView.as_view(url='/', permanent=True)),
    ]
else:
    urlpatterns = [
        url(r'^$', views.index),
        url(r'^tutorial/?$', views.tutorial),
        url(r'^protocol/?$', views.protocol),
        url(r'^license/?$', views.license),
        url(r'^download/?$', views.download),
        url(r'^docs/?$', views.docs),
        url(r'^about/?$', views.about),

        url(r'^result/?$', views.result),
        url(r'^design_1d/?$', wrapper_1d.design_1d),
        url(r'^design_1d_run/?$', wrapper_1d.design_1d_run),
        url(r'^demo_1d/?$', wrapper_1d.demo_1d),
        url(r'^demo_1d_run/?$', wrapper_1d.demo_1d_run),
        url(r'^random_1d/?$', wrapper_1d.random_1d),

        url(r'^design_2d/?$', wrapper_2d.design_2d),
        url(r'^design_2d_run/?$', wrapper_2d.design_2d_run),
        url(r'^demo_2d/?$', wrapper_2d.demo_2d),
        url(r'^demo_2d_run/?$', wrapper_2d.demo_2d_run),
        url(r'^random_2d/?$', wrapper_2d.random_2d),

        url(r'^design_2d_from_1d/?$', wrapper_2d.design_2d_from_1d),

        url(r'^(home|index)/?$', RedirectView.as_view(url='/', permanent=True)),
        url(r'^(help|intro)/?$', RedirectView.as_view(url='/tutorial/', permanent=True)),
        url(r'^(exp|experiment|resource)/?$', RedirectView.as_view(url='/protocol/', permanent=True)),
        url(r'^(readme|copyright)/?$', RedirectView.as_view(url='/license/', permanent=True)),
        url(r'^(package|code|source|repository)/?$', RedirectView.as_view(url='/download/', permanent=True)),
        url(r'^(doc|documentation|reference|manual)/?$', RedirectView.as_view(url='/docs/', permanent=True)),
        url(r'^(citation|contact|primerize)/?$', RedirectView.as_view(url='/about/', permanent=True)),

        url(r'^(find|retrieve)/?$', RedirectView.as_view(url='/result/', permanent=True)),
        url(r'^design/?$', RedirectView.as_view(url='/design_1d/', permanent=True)),
        url(r'^(demo|P4P6|demo_P4P6|example_P4P6)/?$', RedirectView.as_view(url='/demo_1d/', permanent=True)),

        url(r'^login/?$', user.user_login),
        url(r'^logout/?$', user.user_logout),
        url(r'^password/?$', user.user_password),
        url(r'^admin$', RedirectView.as_view(url='/admin/', permanent=True)),

        url(r'^get_js/?$', views.get_js),
        url(r'^get_ver/?$', views.get_ver),
        url(r'^get_user/?$', views.get_user),
        url(r'^get_admin/?$', views.get_admin),

        url(r'^error/400/?$', views.error400),
        url(r'^error/401/?$', views.error401),
        url(r'^error/403/?$', views.error403),
        url(r'^error/404/?$', views.error404),
        url(r'^error/500/?$', views.error500),
        url(r'^error/503/?$', views.error503),

        url(r'^ping_test/?$', views.ping_test),
        url(r'^admin/browse/' + path_end, user.browse),
        url(r'^admin/', include(admin.site.urls)),

        url(r'^site_media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT + '/media'}),
        url(r'^site_data/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT + '/data'}),
        url(r'^LICENSE.md$', serve, kwargs={'path': 'LICENSE.md', 'document_root': MEDIA_ROOT}),
        url(r'^robots.txt$', serve, kwargs={'path': 'robots.txt', 'document_root': MEDIA_ROOT}),
    ]

    if DEBUG: urlpatterns.append(url(r'^test/?$', views.test))

handler400 = views.error400
handler403 = views.error403
handler404 = views.error404
handler500 = views.error500


from django.conf.urls import include, url, handler404, handler500
# from django.conf.urls.static import static
from django.contrib import admin
# from django.contrib.auth.views import login
# from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.views.static import serve

from adminplus.sites import AdminSitePlus
from filemanager import path_end

from src.settings import MEDIA_ROOT, STATIC_ROOT, STATIC_URL, DEBUG
from src import user
from src import views
from src import wrapper_1d

admin.site = AdminSitePlus()
admin.site.index_title = 'Primerize Administration'
admin.autodiscover()
admin.site.login = user.user_login
admin.site.logout = user.user_logout


urlpatterns = [
    url(r'^$', views.index),
    url(r'^tutorial/?$', views.tutorial),
    url(r'^protocol/?$', views.protocol),
    url(r'^license/?$', views.license),
    url(r'^download/?$', views.download),
    url(r'^about/?$', views.about),

    url(r'^result/?$', views.result),
    url(r'^design_1d/?$', wrapper_1d.design_1d),
    url(r'^design_1d_run/?$', wrapper_1d.design_1d_run),
    url(r'^demo_1d/?$', wrapper_1d.demo_1d),
    url(r'^demo_1d_run/?$', wrapper_1d.demo_1d_run),
    url(r'^random_1d/?$', wrapper_1d.random_1d),

    url(r'^home/?$', RedirectView.as_view(url='/', permanent=True)),
    url(r'^index/?$', RedirectView.as_view(url='/', permanent=True)),
    url(r'^help/?$', RedirectView.as_view(url='/tutorial/', permanent=True)),
    url(r'^intro/?$', RedirectView.as_view(url='/tutorial/', permanent=True)),
    url(r'^exp/?$', RedirectView.as_view(url='/protocol/', permanent=True)),
    url(r'^experiment/?$', RedirectView.as_view(url='/protocol/', permanent=True)),
    url(r'^resource/?$', RedirectView.as_view(url='/protocol/', permanent=True)),
    url(r'^readme/?$', RedirectView.as_view(url='/license/', permanent=True)),
    url(r'^copyright/?$', RedirectView.as_view(url='/license/', permanent=True)),
    url(r'^package/?$', RedirectView.as_view(url='/download/', permanent=True)),
    url(r'^repository/?$', RedirectView.as_view(url='/download/', permanent=True)),
    url(r'^citation/?$', RedirectView.as_view(url='/about/', permanent=True)),
    url(r'^contact/?$', RedirectView.as_view(url='/about/', permanent=True)),
    url(r'^primerize/?$', RedirectView.as_view(url='/about/', permanent=True)),

    url(r'^find/?$', RedirectView.as_view(url='/result/', permanent=True)),
    url(r'^retrieve/?$', RedirectView.as_view(url='/result/', permanent=True)),
    url(r'^design/?$', RedirectView.as_view(url='/design_1d/', permanent=True)),
    url(r'^demo/?$', RedirectView.as_view(url='/demo_1d/', permanent=True)),
    url(r'^P4P6/?$', RedirectView.as_view(url='/demo_1d/', permanent=True)),
    url(r'^demo_P4P6/?$', RedirectView.as_view(url='/demo_1d/', permanent=True)),
    url(r'^example_P4P6/?$', RedirectView.as_view(url='/demo_1d/', permanent=True)),

    url(r'^login/?$', user.user_login),
    url(r'^logout/?$', user.user_logout),
    url(r'^password/?$', user.user_password),
    url(r'^admin$', RedirectView.as_view(url='/admin/', permanent=True)),

    url(r'^get_user/?$', views.get_user),
    url(r'^get_admin/?$', views.get_admin),
    url(r'^get_js/?$', views.get_js),

    url(r'^ping_test/?$', views.ping_test),
    url(r'^site_media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT + '/media'}),
    url(r'^site_data/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT + '/data'}),

    url(r'^error/400/?$', views.error400),
    url(r'^error/401/?$', views.error401),
    url(r'^error/403/?$', views.error403),
    url(r'^error/404/?$', views.error404),
    url(r'^error/500/?$', views.error500),

    url(r'^admin/browse/' + path_end, user.browse),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?:LICENSE.md)?$', serve, kwargs={'path': 'LICENSE.md', 'document_root': MEDIA_ROOT}),
    url(r'^(?:robots.txt)?$', serve, kwargs={'path': 'robots.txt', 'document_root': MEDIA_ROOT}),
] #+ static(STATIC_URL, document_root=STATIC_ROOT)

if DEBUG: urlpatterns.append(url(r'^test/$', views.test))
handler404 = views.error404
handler500 = views.error500


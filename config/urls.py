from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls

from cms.search import views as search_views
#from cms.api import api_router
from main import urls as main_urls

from django.apps import apps

# from imgapp import urls as img_urls
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('blog/', include(wagtail_urls), name='blog'),
    path('documents/', include(wagtaildocs_urls)),
    path('checkout/paypal/', include('paypal.express.urls')),

    path('sitemap.xml', sitemap),

    #path('api/', include('leads.urls')),
    #path('api/v2/', api_router.urls),
    #path('__debug__/', include(debug_toolbar.urls)),
]

urlpatterns = urlpatterns + i18n_patterns(
    path('admin/', admin.site.urls),
    path('ontest/', include(main_urls), name='index'),
    path('shop/', include(apps.get_app_config('oscar').urls[0])),
    path('blog-admin/', include(wagtailadmin_urls)),
    path('search/', search_views.search, name="search"),
    path('dashboard/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('support/', include('helpdesk.urls')),

    # examples
    path('portfolio/lawyer/', include('lawyer.urls')),
    #prefix_default_language=False, 
    )

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView
    from django.views.generic.base import RedirectView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path(
            'favicon.ico', RedirectView.as_view(
                url=settings.STATIC_URL + 'img/bread-favicon.ico'
            )
        )
    ]

    # Add views for testing 404 and 500 templates
    urlpatterns += [
        path('test404/', TemplateView.as_view(template_name='404.html')),
        path('test500/', TemplateView.as_view(template_name='500.html')),
    ]

# urlpatterns += [
    
# ]

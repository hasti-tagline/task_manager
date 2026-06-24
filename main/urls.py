from django.contrib import admin
from django.urls import path, include
from .views import *
from accounts.views import LoginAPIView
from rest_framework_simplejwt.views import (TokenRefreshView)

from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi




schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API",
        default_version="v1",
        description="API documentation for Task Manager project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),


    # admin url
    path("admin/",admin.site.urls),

    # apps URLS
    path("",include("accounts.urls")),
    path("",include("tasks.urls")),

    # JWT LOGIn
    path("api/login/",LoginAPIView.as_view(),name="api-login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),


    # TEMPLATE PAGES
    path("",login_page,name="login-page"),
    path("register-page/",register_page,name="register-page"),
    path("dashboard/",dashboard_page,name="dashboard"),
]



if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    # urlpatterns += static(
    #     settings.STATIC_URL,
    #     document_root=settings.STATIC_ROOT
    # )


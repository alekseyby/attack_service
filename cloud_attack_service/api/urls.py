from django.urls import path, include

from .views import (
    AttackView,
    ClodStatView,
)

v1_urls = [
    path('attack/', AttackView.as_view(), name='attack'),
    path('stats/', ClodStatView.as_view(), name='stats')
]


urlpatterns = [
    path('v1/', include(v1_urls)),
]

from django.conf.urls import url, include
from battlelogs import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
#router.register(r'battlelogs',views.BattlelogSet )
router.register(r'players', views.PlayerViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'battlelogs', views.BattlelogViewSet)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

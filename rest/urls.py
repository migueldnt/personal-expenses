from django.urls import include, path
from rest_framework import routers
from .views import AccountVisiblesViewSet

router = routers.DefaultRouter()
router.register(r'accounts', AccountVisiblesViewSet,basename="Accounts")
##router.register(r'all-accounts', AccountVisiblesViewSet)
urlpatterns = [
    path('', include(router.urls)),
]

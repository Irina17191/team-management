from rest_framework import routers

from teams.views import TeamViewSet, PersonViewSet


router = routers.DefaultRouter()
router.register("persons", PersonViewSet)
router.register("teams", TeamViewSet)

urlpatterns = router.urls

app_name = "teams"

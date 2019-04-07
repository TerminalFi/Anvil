from rest_framework import routers
from django.urls import include, path
from .views import (index, AnvilJobViewSet) #TargetsViewSet, ScansViewSet, ResultsViewSet,)

app_name = 'sdb'

router = routers.DefaultRouter()
router.register('jobs', AnvilJobViewSet)
# router.register('jobs/<uuid:job_uuid>', AnvilJobViewSet)
# router.register('scans', ScansViewSet)
# router.register('scans/<int:uuid>', ScansViewSet)
# router.register('results', ResultsViewSet)
# router.register('results/<int:uuid>', ResultsViewSet)

urlpatterns = [
    path('scans/', index, name='index'),
    path('api/', include(router.urls)),
]

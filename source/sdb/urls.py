from rest_framework import routers
from django.urls import include, path
from django.views.generic import TemplateView
from .views import (scan_overview, AnvilJobViewSet, scan_stats) #TargetsViewSet, ScansViewSet, ResultsViewSet,)

app_name = 'sdb'

router = routers.DefaultRouter()
router.register('scans', AnvilJobViewSet)
# router.register('jobs/<uuid:job_uuid>', AnvilJobViewSet)
# router.register('scans', ScansViewSet)
# router.register('scans/<int:uuid>', ScansViewSet)
# router.register('results', ResultsViewSet)
# router.register('results/<int:uuid>', ResultsViewSet)

urlpatterns = [
    path('scans/', scan_overview, name='scan_overview'),
    path('scan/stats/', scan_stats, name='scan_stats'),
    path('api/', include(router.urls)),
    path("1/",
        TemplateView.as_view(template_name="sdb/application.html"),
        name="app",
    ),
]

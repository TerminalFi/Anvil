import json
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from rest_framework import viewsets
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from celery.task.control import revoke

from .models import anvil_job  # Target, Scans, Results
from .serializers import AnvilJobSerializer # TargetSerializer, ScansSerializer, ResultsSerializer
from .tasks import scan_host


def scan_overview(request):
    jobs = anvil_job.objects.all()
    completed_jobs = jobs.filter(job_status="completed").count()
    running_jobs = jobs.filter(job_status="running").count()
    terminated_jobs = jobs.filter(job_status="terminated").count()
    return render(request, "sdb/default.html", context={
        'jobs': jobs,
        'total_jobs': jobs.count(),
        'completed_jobs': completed_jobs,
        'running_jobs': running_jobs,
        'terminated_jobs': terminated_jobs})


def scan_stats(request):
    jobs = anvil_job.objects.all()
    completed_jobs = jobs.filter(job_status="completed").count()
    running_jobs = jobs.filter(job_status="running").count()
    terminated_jobs = jobs.filter(job_status="terminated").count()
    return JsonResponse({
        'completed_jobs': {'name': 'Completed Scans', 'value': completed_jobs},
        'running_jobs': {'name': 'Running Scans', 'value': running_jobs},
        'terminated_jobs': {'name': 'Terminated Scans', 'value': terminated_jobs},
        'total_jobs': {'name': 'Total Scans', 'value': jobs.count()}})


class AnvilJobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Create, Delete, Viewing of Scans
    """
    queryset = anvil_job.objects.all().order_by('id')
    serializer_class = AnvilJobSerializer
    lookup_field = 'job_uuid'


# class ResultsViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows Create, Delete, Viewing of Results
#     """
#     queryset = Results.objects.all()
#     serializer_class = ResultsSerializer
#     lookup_field = 'uuid'

import json
from django.http import JsonResponse
from rest_framework import filters
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
        'completed_scans': {'name': 'Completed Scans', 'value': completed_jobs},
        'running_scans': {'name': 'Running Scans', 'value': running_jobs},
        'terminated_scans': {'name': 'Terminated Scans', 'value': terminated_jobs},
        'total_scans': {'name': 'Total Scans', 'value': jobs.count()}})


# def scan_archive(request):
#     if request.is_ajax() && request.POST:
#         scans = request.POST.get('data')
#         for scan in scans:
#             if anvil_job.objects.filter(job_uuid=scan.job_uuid).exists():
#                 job = anvil_job.objects.get(job_uuid=scan.job_uuid)
#                 job.job_archived = True
#                 job.save()

#     return JsonResponse({
#         'status': True })


class AnvilJobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Create, Delete, Viewing of Scans
    """
    queryset = anvil_job.objects.all().order_by('id')
    serializer_class = AnvilJobSerializer
    lookup_field = 'job_uuid'
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('job_name', 'job_uuid', 'job_status',)
    ordering_fields = ('job_name', 'job_uuid', 'job_status',)


# class ResultsViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows Create, Delete, Viewing of Results
#     """
#     queryset = Results.objects.all()
#     serializer_class = ResultsSerializer
#     lookup_field = 'uuid'

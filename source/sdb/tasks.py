from celery import task, current_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
import nmap
from .models import anvil_job, anvil_target

nmap_scans = {'fast_tcp': '-Pn -F -T4 -vvvv',
              'full_tcp': '-Pn -sV -sC -O -p- -T4 -vvvvv',
              'fast_udp': '-n -Pn -sU -F --min-rate=1000 -vvvvv',
              'quick_udp': '-n -Pn -sU --min-rate=1000 -vvvvv',
              'full_udp': '-n -Pn -sU -p- -T4 -vvvvv'}

staged_nmap_scans = {'1': '-Pn -T4 -sV -p T:80,443',
                     '2': '-Pn -T4 -sV -O -p T:25,135,137,139,445,1433,3306,5432,U:137,161,162,1434',
                     '3': '-Pn -T4 -sV -p T:23,21,22,110,111,2049,3389,8080,U:500,5060'}
                     
fields = ['hostnames', 'addresses', 'vendor', 'status',
          'tcp', 'udp']
# '-Pn -T4 -sV -p T:0-20,24,26-79,81-109,112-134,136,138,140-442,444,446-1432,1434-2048,2050-3305,3307-3388,3390-5431,5433-8079,8081-29999',
# '-Pn -T4 -sV -p T:30000-65535']


@task(bind=True)
def scan_host(self, job_id, target_id):
    job = anvil_job.objects.get(pk=job_id)
    target = anvil_target.objects.get(pk=target_id)

    current_task.update_state(state='PROGRESS',
                              meta={'status': 'scanning', 'scan_command': ''})
    channel_layer = get_channel_layer()
    job.job_status = "started"
    job.save()

    async_to_sync(channel_layer.group_send)(
        'ws_scans',
        {
            'type': 'scan.event',
            'content': {
                "action": job.job_status,
                "job_id": job.id,
                "job_uuid": str(job.job_uuid),
                "job_name": job.job_name,
                "job_status": job.job_status
            }
        }
    )
    nm = nmap.PortScanner()
    final_results = dict()

    job.job_status = 'running'
    job.save()
    async_to_sync(channel_layer.group_send)(
        'ws_scans',
        {
            'type': 'scan.event',
            'content': {
                "action": job.job_status,
                "job_id": job.id,
                "job_uuid": str(job.job_uuid),
                "job_name": job.job_name,
                "job_status": job.job_status,
                "current_stage": {'stage': job.job_stage }
            }
        }
    )
    for k, v in staged_nmap_scans.items():
        job.job_stage = k
        job.save()
        results = nm.scan(target.target_ip, arguments=v)
        final_results[k] = results
        async_to_sync(channel_layer.group_send)(
            'ws_scans',
            {
                'type': 'scan.event',
                'content': {
                    "action": job.job_status,
                    "job_id": job.id,
                    "job_uuid": str(job.job_uuid),
                    "job_name": job.job_name,
                    "job_status": job.job_status,
                    "current_stage": {'stage': k, 'results': results['scan']}

                }
            }
        )

    # job.status = "completed"
    job.job_status = "completed"
    job.job_finish_time = timezone.now()
    job.save()
    async_to_sync(channel_layer.group_send)(
        'ws_scans',
        {
            'type': 'scan.event',
            'content': {
                "action": job.job_status,
                "job_id": job.id,
                "job_uuid": str(job.job_uuid),
                "job_name": job.job_name,
                "job_status": job.job_status
                # "job_results": {k : v['scan'] for k, v in final_results.items()}

            }
        }
    )

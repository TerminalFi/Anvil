from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from channels.layers import get_channel_layer
from celery.task.control import revoke
import json

from .models import anvil_job, anvil_target
from .tasks import scan_host
from core.celery import app


class ScanConsumer(JsonWebsocketConsumer):

    def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            'ws_scans',
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'ws_scans',
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        text_data_json = json.loads(text_data)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            'ws_scans',
            {
                'type': 'scan.start',
                'message': text_data_json
            }
        )

    def scan_start(self, event):
        data = event['message']
        if data:
            if data['action'] == 'start_work':
                start_work(data)
            elif data['action'] == 'stop_work':
                stop_work(data)

    def scan_event(self, event):
        self.send_json(
            {
                'type': 'scan.event',
                'content': event['content']
            }
        )


def start_work(data):
    """
        Future Plan, Break out logic for multiple targets.
        For each IP in range, create a new target,
        associated with the same scan. Create a task per target ?
        Perhaps create a subtask under than main Celery Task and split
        targets out there.
    """
    channel_layer = get_channel_layer()
    if data['job_name'] == '' or data['target'] == '':
        async_to_sync(channel_layer.group_send)(
            'ws_scans',
            {
                'type': 'scan.event',
                'content': {
                        "action": "error",
                        "message": 'Invalid Scan Information'
                }
            }
        )
        return
    # Create Job
    job = anvil_job()
    job.job_name = data['job_name']
    job.job_target = data['target']
    job.job_status = "initialization"
    job.save()

    # Create Target
    target = anvil_target(
        job=job, target_ip=data['target'])
    target.save()

    # Send task to Celery Workers
    scan_host_task = scan_host.delay(job.id, target.id)

    # Update Job with Celery Task ID
    job.job_celery_id = scan_host_task.id
    job.save()

    # Send update to UI
    async_to_sync(channel_layer.group_send)(
        'ws_scans',
        {
            'type': 'scan.event',
            'content': {
                    "action": "initialization",
                    "job_id": job.id,
                    "job_name": job.job_name,
                    "job_status": job.job_status,
            }
        }
    )


def stop_work(data):
    """
        Future Plan, Break out logic for multiple targets.
    """
    # Create Job
    job_id = data['job_id']
    try:
        job_id = int(job_id)
    except:
        return

    job = anvil_job.objects.get(pk=job_id)
    if job.job_status != 'completed' and job.job_status != 'terminated':
        revoke(job.job_celery_id, terminate=True)
        job.job_status = 'terminated'
        job.save()

    # Send update to UI
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'ws_scans',
        {
            'type': 'scan.event',
            'content': {
                "action": job.job_status,
                "job_id": job.id,
                "job_status": job.job_status,
            }
        })
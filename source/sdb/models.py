from uuid import uuid4
from django.db import models
from django.utils import timezone


class anvil_job(models.Model):
    job_name = models.CharField(max_length=128, blank=True)
    job_uuid = models.UUIDField(default=uuid4)
    job_start_time = models.DateTimeField(default=timezone.now)
    job_finish_time = models.DateTimeField(default=timezone.now)
    job_completed = models.DateTimeField(null=True, blank=True)
    job_nmap_version = models.CharField(max_length=64, blank=True)
    job_scan_args = models.CharField(max_length=128, blank=True)
    job_target = models.TextField(blank=True)
    job_total_hosts = models.TextField(blank=True)
    job_online_hosts = models.TextField(blank=True)
    job_offline_hosts = models.TextField(blank=True)
    job_status = models.CharField(max_length=64, blank=True)
    job_stage = models.CharField(max_length=64, default=0)
    job_celery_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return self.name

class anvil_target(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False)
    target_checked = models.CharField(max_length=255)
    target_os_match = models.CharField(max_length=255)
    target_os_accuracy = models.CharField(max_length=255)
    target_ip = models.CharField(max_length=255)
    target_ipv4 = models.CharField(max_length=255)
    target_ipv6 = models.CharField(max_length=255)
    target_mac = models.CharField(max_length=255)
    target_status = models.CharField(max_length=255)
    target_hostname = models.CharField(max_length=255)
    target_vendor = models.CharField(max_length=255)
    target_uptime = models.CharField(max_length=255)
    target_lastboot = models.CharField(max_length=255)
    target_distance = models.IntegerField(default=0)
    target_state = models.CharField(max_length=255)
    target_count = models.IntegerField(default=0)
    os = models.ManyToManyField('anvil_os')
    port = models.ManyToManyField("anvil_port")
    job = models.ForeignKey(anvil_job, on_delete=models.CASCADE)


class anvil_os(models.Model):
    os_name = models.CharField(max_length=255)
    os_family = models.CharField(max_length=255)
    os_generation = models.CharField(max_length=255)
    os_type = models.CharField(max_length=255)
    os_vendor = models.CharField(max_length=255)
    os_accuracy = models.CharField(max_length=255)
    target = models.ForeignKey(anvil_target, on_delete=models.CASCADE)


class anvil_port(models.Model):
    port_id = models.CharField(max_length=255)
    port_protocol = models.CharField(max_length=255)
    port_state = models.CharField(max_length=255)
    target = models.ForeignKey(anvil_target, on_delete=models.CASCADE)


class anvil_script(models.Model):
    script_id = models.IntegerField(default=0)
    script_output = models.TextField(blank=True)
    target = models.ForeignKey(anvil_target, on_delete=models.CASCADE)
    port = models.ForeignKey(anvil_port, on_delete=models.CASCADE)


class anvil_service(models.Model):
    service_name = models.CharField(max_length=255)
    service_product = models.CharField(max_length=255)
    service_version = models.CharField(max_length=255)
    service_extra = models.CharField(max_length=255)
    service_fingerprint = models.CharField(max_length=255)
    port = models.ForeignKey(anvil_port, on_delete=models.CASCADE)




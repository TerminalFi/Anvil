from .models import anvil_job
from rest_framework import serializers


# class TargetSerializer(serializers.HyperlinkedModelSerializer):
# 	scans = serializers.SlugRelatedField(
#         many=True,
#         read_only=True,
#         slug_field='uuid'
#     )
# 	class Meta:
# 		model = Target
# 		fields = ('target', 'uuid', 'id', 'scans')
# 		lookup_field = 'uuid'
# 		extra_kwargs = {
# 		    'url': {'lookup_field': 'uuid'}
# 		}


class AnvilJobSerializer(serializers.ModelSerializer):

	class Meta:
	    model = anvil_job
	    exclude = ('id',)
	    lookup_field = 'job_uuid'
	    extra_kwargs = {
		    'url': {'lookup_field': 'job_uuid'}
		}

# class ResultsSerializer(serializers.HyperlinkedModelSerializer):
# 	scan = serializers.SlugRelatedField(
# 	     queryset= Target.objects.all(),
# 	     slug_field='uuid'
# 	 )
# 	class Meta:
# 		model = Results
# 		fields = ('scan', 'results')
# 		lookup_field = 'uuid'
# 		extra_kwargs = {
# 		    'url': {'lookup_field': 'uuid'}
# 		}

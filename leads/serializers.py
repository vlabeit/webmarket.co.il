from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lead
        fields = ('id', 'url', 'name', 'paradigm')
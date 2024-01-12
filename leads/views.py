from django.shortcuts import render
from rest_framework import viewsets
from .models import Lead
from .serializers import LeadSerializer

class LeadView(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
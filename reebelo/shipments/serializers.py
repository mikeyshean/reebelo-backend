from rest_framework import serializers

from reebelo.shipments.models import TrackingCompany


class TrackingCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingCompany
        fields = ("id", "name")

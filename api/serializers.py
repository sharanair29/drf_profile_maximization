from rest_framework import serializers
from .models import Contracts


class ContractsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contracts
        fields = '__all__'

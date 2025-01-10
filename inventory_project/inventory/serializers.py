from rest_framework import serializers
from .models import InventoryItem, InventoryLog
from django.contrib.auth.models import User

class InventoryItemSerializer(serializers.ModelSerializer):
    managed_by = serializers.CharField(source='managed_by.username', read_only=True)  # Return managed_by as username

    class Meta:
        model = InventoryItem
        fields = '__all__'
        read_only_fields = ['managed_by']

class InventoryLogSerializer(serializers.ModelSerializer):
    changed_by = serializers.CharField(source='changed_by.username', read_only=True)  # Return changed_by as username

    class Meta:
        model = InventoryLog
        fields = [
            'id', 'change_type', 'change_reason', 'quantity_before', 'quantity_after', 
            'timestamp', 'item', 'item_name', 'changed_by'  # Expose item_name directly
        ]
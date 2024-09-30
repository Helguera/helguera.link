"""
Serializers for link API
"""
import string
import random
from rest_framework import serializers

from shortener.models import Link


class LinkSerializer(serializers.ModelSerializer):
    """Serializer for links"""

    class Meta:
        model = Link
        fields = ['id', 'short_url', 'original_url', 'times_accessed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'short_url', 'times_accessed', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        
        return super().create(validated_data)
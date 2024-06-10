from rest_framework import serializers

from brons.models import Bron


class BronSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    bron_time_end = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    bron_time_start = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Bron
        fields = '__all__'
        read_only_fields = ('price_for_hour', 'created_at', 'user',
                            'full_price', 'is_active', 'is_confirmed',
                            'status', 'bron_time_end')

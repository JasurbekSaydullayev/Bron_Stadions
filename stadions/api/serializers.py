from rest_framework import serializers

from stadions.models import Stadion


class StadionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    contact = serializers.CharField(read_only=True)

    class Meta:
        model = Stadion
        fields = ('id', 'name', 'contact', 'address', )


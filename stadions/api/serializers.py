from rest_framework import serializers

from stadions.models import Stadion, Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class StadionSerializer(serializers.ModelSerializer):
    contact = serializers.CharField(read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Stadion
        fields = ('id', 'name', 'contact', 'price', 'address', 'location_lat', 'location_lng', 'photos')

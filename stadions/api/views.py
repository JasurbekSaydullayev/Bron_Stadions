from django.db import connection
from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from stadions.api.permissions import IsAdminOrOwner, IsAdminOrOwnerStadion
from stadions.api.serializers import StadionSerializer, PhotoSerializer
from stadions.models import Stadion, Photo
from brons.models import Bron
from pagination import StandardResultsSetPagination
from math import radians, sin, cos, sqrt, atan2
import pytz


class StadionViewSet(viewsets.ModelViewSet):
    queryset = Stadion.objects.all()
    serializer_class = StadionSerializer
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['create', 'destroy', 'put']:
            return [IsAdminOrOwner()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM stadions_stadion WHERE name = %s AND owner_id = %s",
                [serializer.validated_data['name'], request.user.id]
            )
            count = cursor.fetchone()[0]
            if count > 0:
                return Response(
                    {"message": "Sizda ushbu nom bilan oldin stadion ro'yhatdan o'tgan"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, contact=self.request.user.phone_number)

    def list(self, request, *args, **kwargs):
        time_start = request.query_params.get('time_start')
        time_end = request.query_params.get('time_end')
        user_lat = request.query_params.get('user_lat')
        user_lng = request.query_params.get('user_lng')

        queryset = self.filter_queryset(self.get_queryset())

        if time_start and time_end:
            try:
                time_start = timezone.datetime.fromisoformat(time_start.replace('Z', ''))
                time_end = timezone.datetime.fromisoformat(time_end.replace('Z', ''))
                time_start = timezone.make_aware(time_start, pytz.UTC)
                time_end = timezone.make_aware(time_end, pytz.UTC)
            except ValueError as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            available_stadions = []
            for stadion in queryset:
                if not Bron.objects.filter(
                        Q(stadion=stadion) &
                        (Q(bron_time_start__lt=time_end) & Q(bron_time_end__gt=time_start))
                ).exists():
                    available_stadions.append(stadion)
            queryset = Stadion.objects.filter(id__in=[s.id for s in available_stadions])

        if user_lat and user_lng:
            user_lat, user_lng = float(user_lat), float(user_lng)
            for stadion in queryset:
                stadion.distance = self.calculate_distance(user_lat, user_lng, stadion.location_lat,
                                                           stadion.location_lng)
            queryset = sorted(queryset, key=lambda stadion: stadion.distance)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # so'rov yuborish uchun namuna
        # http://127.0.0.1:8000/api/stadions/?time_start=2024-06-10T10:00:00Z&time_end=2024-06-10T12:00:00Z&user_lat=41.353827&user_lng=69.345423

    def calculate_distance(self, user_lat, user_lng, stadion_lat, stadion_lng):
        R = 6371.0
        lat1 = radians(user_lat)
        lon1 = radians(user_lng)
        lat2 = radians(stadion_lat)
        lon2 = radians(stadion_lng)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['post', 'put', 'delete']
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update']:
            return [IsAdminOrOwnerStadion()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.utils import timezone

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from brons.api.permissions import IsAdminOrStadionOwner
from brons.api.serializers import BronSerializer
from brons.models import Bron
from pagination import StandardResultsSetPagination
from stadions.models import Stadion


class BronViewSet(viewsets.ModelViewSet):
    queryset = Bron.objects.all()
    serializer_class = BronSerializer
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'put', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        stadion = serializer.validated_data.get('stadion')
        if not stadion:
            return Response({"message": "Kiritilgan stadion topilmadi"},
                            status=status.HTTP_404_NOT_FOUND)

        time_start = serializer.validated_data.get('bron_time_start')
        hours = serializer.validated_data.get('hours')
        finish_time = time_start + timezone.timedelta(hours=hours)

        brons = stadion.brons.filter(is_active=True).all()
        for bron in brons:
            if bron.bron_time_start < finish_time and bron.bron_time_end > time_start:
                return Response({"message": "Stadion kiritilgan vaqtda bo'sh emas"},
                                status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        if request.user.type == "customer":
            brons = Bron.objects.filter(user=request.user).order_by('-id')
        elif request.user.type == "owner":
            stadions = Stadion.objects.filter(owner=request.user)
            brons = Bron.objects.filter(stadion__in=stadions).order_by('-id')
        elif request.user.is_superuser:
            brons = Bron.objects.all().order_by('-id')
        else:
            brons = Bron.objects.none()

        page = self.paginate_queryset(brons)
        if page is not None:
            serializer = self.get_paginated_response(BronSerializer(page, many=True).data)
        else:
            serializer = BronSerializer(brons, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        price_for_hour = serializer.validated_data['price_for_hour'] = serializer.validated_data[
            'stadion'].price
        hours = serializer.validated_data['hours']
        full_price = price_for_hour * hours
        bron_time_end = serializer.validated_data['bron_time_start'] + timezone.timedelta(hours=hours)
        serializer.save(user=self.request.user, full_price=full_price, bron_time_end=bron_time_end)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        bron = self.get_object()
        bron.is_active = False
        bron.is_confirmed = False
        if request.user.type == "customer":
            bron.status = 'Cancel from Customer'
            bron.save()
            return Response({"message": f"{bron.id} - Bron buyurtmachi tomonidan bekor qilindi"},
                            status=status.HTTP_200_OK)
        elif request.user.type == "owner":
            bron.status = 'Cancel from Owner'
            bron.save()
            return Response({'message': f'{bron.id} - Bron maydon egasi tomonidan bekor qilindi'},
                            status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrStadionOwner])
    def confirm(self, request, pk=None):
        bron = self.get_object()
        if bron.is_confirmed:
            return Response({"message": "Ushbu bron tasdiqlanib bo'lingan"},
                            status=status.HTTP_200_OK)
        bron.is_confirmed = True
        bron.status = "Tasdiqlangan"
        bron.save()
        return Response({'message': f"{bron.id} - Bron maydon egasi tomonidan tasdqilandi"},
                        status=status.HTTP_200_OK)

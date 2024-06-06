from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from stadions.models import Stadion


class StadionViewSet(viewsets.ModelViewSet):
    queryset = Stadion.objects.all()

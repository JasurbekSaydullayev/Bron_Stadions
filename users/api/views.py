from rest_framework import viewsets, status

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.api.pagination import StandardResultsSetPagination
from users.api.permissions import IsOwnerOrReadOnly
from users.api.serializers import UserSerializer
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    pagination_class = StandardResultsSetPagination
    lookup_field = 'phone_number'

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['put', 'delete', 'retrieve']:
            return [IsOwnerOrReadOnly()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        if request.user.type == "customer" or request.user.type == "owner":
            user = User.objects.get(pk=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.user.is_superuser:
            users = User.objects.all()
            page = self.paginate_queryset(users)
            if page is not None:
                serializer = self.get_paginated_response(UserSerializer(page, many=True).data)
            else:
                serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

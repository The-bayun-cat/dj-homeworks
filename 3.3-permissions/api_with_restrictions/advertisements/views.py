from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer

from advertisements.permissions import IsOwnerOrReadOnly

from advertisements.filters import AdvertisementFilter
from django_filters.rest_framework import DjangoFilterBackend


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter



    def get_permissions(self):
        """Получение прав для действий."""
        if self.request.method in SAFE_METHODS:
            # Для просмотра не нужна авторизация
            return []

            # Для создания объявлений нужна авторизация
        elif self.action == "create":
            return [IsAuthenticated()]

            # Для обновления/удаления нужна авторизация + проверка владельца
        else:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
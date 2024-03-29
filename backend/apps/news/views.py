from rest_framework.viewsets import ModelViewSet

from apps.news.models import News
from apps.news.permissions import IsAdminOrReadOnly
from apps.news.serializers import NewsSerializer


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    http_method_names = ['get']

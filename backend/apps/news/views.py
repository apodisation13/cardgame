from apps.news.models import News
from apps.news.permissions import IsAdminOrReadOnly
from apps.news.serializers import NewsSerializer
from rest_framework.viewsets import ModelViewSet


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnly, ]

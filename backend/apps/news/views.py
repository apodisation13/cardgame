from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from apps.news.models import News
from apps.news.serializers import NewsSerializer
from apps.news.permissions import IsAdminOrReadOnly


class NewsView(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOrReadOnly, ]



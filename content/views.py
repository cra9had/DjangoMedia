import operator
from functools import reduce

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tag, MediaContent
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TagFilter
from .serializers import TagSerializer, MediaContentSerializer


class GetMediaContentAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MediaContentSerializer

    def get_queryset(self):
        tags = self.request.data.get("tags")
        tag_ids = []
        for tag in tags:
            try:
                tag_id = Tag.objects.get(body=tag["body"]).id
            except Tag.DoesNotExist:
                continue
            tag_ids.append(tag_id)
        print(reduce(operator.and_, (Q(tags__in=[tag_id]) for tag_id in tag_ids)))
        # return MediaContent.objects.filter(reduce(operator.and_, (Q(tags__body__contains=body) for body in bodies))).distinct()
        # return MediaContent.objects.filter(reduce(operator.and_, (Q(tags__in=[tag_id]) for tag_id in tag_ids))).distinct()
        return MediaContent.objects.filter(tags__id__in=tag_ids).distinct()

    def post(self, request):
        try:
            query = self.get_queryset()
        except Exception as r:
            print(r)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data)


class GetTagsAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TagFilter
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.all()

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tag, MediaContent, ChosenMediaContent
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TagFilter
from .serializers import TagSerializer, MediaContentSerializer, ChoiceMediaContentSerializer, GetChosenMediaSerializer


class ChoiceMediaAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChoiceMediaContentSerializer

    def get_queryset(self):
        return ChosenMediaContent.objects.filter(user=self.request.user)

    def get(self, request):
        serializer = GetChosenMediaSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response()


class GetMediaContentAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MediaContentSerializer

    def get_queryset(self):
        tags = self.request.data.get("tags")
        objects = MediaContent.objects
        for tag in tags:
            objects = objects.filter(tags__body__contains=tag["body"])
        return objects.distinct()

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

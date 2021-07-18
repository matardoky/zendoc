from decimal import Context
from django.shortcuts import render
from django.db.models import Avg, Count

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

from articles.models import Article
from articles.renderers import ArticleJSONRenderer
from articles.serializers import ArticleSerializer

class LargeResultsSetPagination(PageNumberPagination):
    
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

class ArticleViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin, 
    GenericViewSet
    ):

    lookup_field = 'slug'
    queryset =Article.objects.annotate(
        average_rating = Avg("rating__stars")
    )
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes   = (ArticleJSONRenderer,)
    serializer_class   =  ArticleSerializer
    paginate_class     =  LargeResultsSetPagination

    def create(self, request):

        article = request.data.get('article', {})
        serializer = self.serializer_class(data=article)
        serializer.is_valid()(raise_exception=True)
        serializer.save(author=request.user.profile)

        return Response(serializer.data, status = HTTP_201_CREATED) 

    def list(self, request):

        queryset = Article.objects.all()
        serializer_context = {'request':request}
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(
                page, 
                context = serializer_context,
                many=True
            )
            output = self.get_paginated_response(serializer.data)
        else: 
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status = HTTP_200_OK)
            
        return output

    def  retrieve(self, request, slug):
        serializer_context = {'request': request}
        try: 
            serializer_instance = self.queryset.get(slug=slug)

        except Article.DoesNotExist:
            raise NotFound("An article with this slug doesn't exist")

        serializer = self.serializer_class(
            serializer_instance,
            context = serializer_context
        )
        return Response(serializer.data, status = HTTP_200_OK)

    
    def update(self, request, slug):

        serializer_context = {'request': request}

        try: 
            serializer_instance = self.queryset.get(slug=slug)

        except Article.DoesNotExist:
            raise NotFound("An article with this slug doesn't exist")

        if not serializer_instance.author_id == request.user.profile.id:
            raise PermissionDenied("You are not authorizedto edit this article.")

        serializer_data = request.data.get('article',)
        serializer = self.serializer_class(
            serializer_instance,
            context = serializer_context,
            data = serializer_data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status = HTTP_200_OK)

    def destroy(self, request, slug):

        try:
            article = self.queryset.get(slug=slug)

        except Article.DoesNotExist:
            raise NotFound("An article with this slug doesn't exist")    

        if article.author_id == request.user.profile.id:
            article.delete()
        else:
            raise PermissionDenied(
                "You are not authorizedto edit this article."
            )
        
        return Response(None, status = HTTP_204_NO_CONTENT)

    
    def get_queryset(self):
        queryset = self.queryset

        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__tag=tag)

        return queryset






    
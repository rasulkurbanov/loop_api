from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics



# Create your views here.
#Add generics, mixins based Class Api Views
class GenericListView(generics.GenericAPIView,
                    mixins.ListModelMixin, 
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin, 
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin):

    serializer_class = ArticleSerializer
    queryset = Article.objects.all()       

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request)
        else:
            return self.list(request)
    


    def post(self, request):
        return self.create(request)

    def put(self, request, pk=None):
        return self.update(request)


    def delete(self, request, pk=None):
        return self.destroy(request)
















class ArticleListView(APIView):

    def get(self, request):
        articles = Article.objects.all()  
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)        

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status==status.HTTP_404_NOT_FOUND)              



class ArticleDetailView(APIView):

    def get_object(self, pk):
        try:
            return Article.objects.get(id=pk)  
        except Article.DoesNotExist as exc:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND) 


    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def article_list(request):

    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


    elif request.method == "POST":
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status==status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail (request, pk):
    try:
      article = Article.objects.get(id=pk)
    except Article.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == "GET":
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    
    elif request.method == "PUT":
        serializer = ArticleSerializer(article, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    elif request.method == "DELETE":
        article.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


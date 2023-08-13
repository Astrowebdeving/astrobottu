from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Question, Qusers
from .serializers import RandomQuestionSerializer, QusersReturn
class RandomQuestion(APIView):
    def get(self, request, format=None, **kwargs):
        question = Question.objects.filter().order_by('?')[:1]
        serializer = RandomQuestionSerializer(question, many=True)
        return Response(serializer.data)
class AllUsers(APIView):
    def get(self, request, format=None, **kwargs):
        users = Qusers.objects.filter().order_by("Total Points")
        serializerAU = QusersReturn(users, many = True)
        return Response(serializerAU.data)
class TopUsers(APIView):
    def get(self, request, format=None, **kwargs):
        users = Qusers.objects.filter().order_by("Total Points")[:10]
        serializerTU = QusersReturn(users,many = True)
        return Response(serializerTU.data)
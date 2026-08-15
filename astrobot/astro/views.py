import secrets

from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.views import APIView

from .models import Question, Qusers
from .serializers import RandomQuestionSerializer, QusersReturn


class RandomQuestion(APIView):
    def get(self, request, format=None, **kwargs):
        supplied_key = request.headers.get("X-API-Key", "")
        if settings.BOT_API_KEY and not secrets.compare_digest(
            supplied_key, settings.BOT_API_KEY
        ):
            return Response(
                {"detail": "Valid X-API-Key header required."},
                status=HTTP_403_FORBIDDEN,
            )

        # inactive questions stay available in admin but not in games
        question = Question.objects.filter(is_active=True).order_by("?")[:1]
        serializer = RandomQuestionSerializer(question, many=True)
        return Response(serializer.data)


class AllUsers(APIView):
    def get(self, request, format=None, **kwargs):
        users = Qusers.objects.order_by("-totalpoints", "username")
        serializer = QusersReturn(users, many=True)
        return Response(serializer.data)


class TopUsers(APIView):
    def get(self, request, format=None, **kwargs):
        users = Qusers.objects.order_by("-totalpoints", "username")[:10]
        serializer = QusersReturn(users, many=True)
        return Response(serializer.data)

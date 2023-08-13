from rest_framework import serializers
from .models import Question, Answer, Qusers

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'answer',
            'is_correct',
        ]

class RandomQuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True, read_only = True)
    class Meta:
        model = Question 
        fields = [
            'title', 'points', 'answer',
        ]

class QusersReturn(serializers.ModelSerializer):
    class Meta:
        model = Qusers
        fields = [
            'username', 'totalpoints' 
        ]
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
        users = Qusers.objects.filter().order_by("totalpoints")
        serializerAU = QusersReturn(users, many = True)
        return Response(serializerAU.data)
class TopUsers(APIView):
    def get(self, request, format=None, **kwargs):
        users = Qusers.objects.filter().order_by("totalpoints")[:10]
        serializerTU = QusersReturn(users,many = True)
        return Response(serializerTU.data)
    
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            binary_data = image.read()  # Read the binary data from the image file
            Question.objects.create(optional_image=binary_data)
    images = Question.objects.all()
    return render(request, 'image_upload.html', {'images': images})
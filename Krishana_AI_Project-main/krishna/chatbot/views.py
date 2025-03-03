from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import QuestionAnswer

@api_view(['POST'])
def get_mythology_answer(request):
    question = request.data.get('question')
    try:
        answer = QuestionAnswer.objects.get(question_text=question).answer_text
    except QuestionAnswer.DoesNotExist:
        answer = "Sorry, I don't have an answer for that."

    return Response({"answer": answer})




from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

def signin(request):
    return render(request, 'signin.html')
def signup(request):
    return render(request, 'signup.html')
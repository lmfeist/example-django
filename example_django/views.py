from django.shortcuts import render
from django.http import HttpResponse
import datetime


def home(request):
    """Home view with htmx functionality."""
    return render(request, 'home.html')


def get_current_time(request):
    """HTMX endpoint that returns the current time."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse(f"<p class='text-blue-600 font-semibold'>Current time: {current_time}</p>")


def greet(request):
    """HTMX endpoint that returns a greeting."""
    name = request.GET.get('name', 'Guest')
    return HttpResponse(f"<div class='p-4 bg-green-100 rounded-lg'><p class='text-green-800'>Hello, {name}! Welcome to the HTMX demo.</p></div>")

from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
import datetime
import time
import json


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


def sse_stream(request):
    """Server-Sent Events endpoint that streams updates."""
    def event_stream():
        """Generator function that yields SSE formatted data."""
        for i in range(10):  # Send 10 updates
            # Get current timestamp
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            
            # Create the HTML content to send
            html_content = f'<div class="alert alert-info mb-2">Update #{i + 1} at {current_time}</div>'
            
            # Format as SSE
            # SSE format: "data: <content>\n\n"
            yield f"data: {html_content}\n\n"
            
            # Wait 1 second before sending next update
            time.sleep(1)
        
        # Send a final message
        final_html = '<div class="alert alert-success">Stream completed!</div>'
        yield f"data: {final_html}\n\n"
    
    # Return StreamingHttpResponse with SSE content type
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'  # Disable buffering in nginx
    return response

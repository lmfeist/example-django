from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import datetime
import json


def home(request):
    """Home view with htmx functionality."""
    # Initialize session todos if not exists
    if 'todos' not in request.session:
        request.session['todos'] = [
            {'id': 1, 'text': 'Learn HTMX basics', 'completed': True},
            {'id': 2, 'text': 'Build dynamic UI without JavaScript', 'completed': False},
            {'id': 3, 'text': 'Deploy to production', 'completed': False},
        ]
        request.session['next_id'] = 4
    return render(request, 'home.html')


def get_current_time(request):
    """HTMX endpoint that returns the current time."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse(f"<p class='text-blue-600 font-semibold'>Current time: {current_time}</p>")


def greet(request):
    """HTMX endpoint that returns a greeting."""
    name = request.GET.get('name', 'Guest')
    return HttpResponse(f"<div class='p-4 bg-green-100 rounded-lg'><p class='text-green-800'>Hello, {name}! Welcome to the HTMX demo.</p></div>")


# Todo List HTMX Endpoints

def get_todos(request):
    """Get all todos with optional filtering."""
    todos = request.session.get('todos', [])
    filter_type = request.GET.get('filter', 'all')
    
    if filter_type == 'active':
        todos = [t for t in todos if not t['completed']]
    elif filter_type == 'completed':
        todos = [t for t in todos if t['completed']]
    
    html = render_todo_list(todos, filter_type)
    return HttpResponse(html)


def add_todo(request):
    """Add a new todo item."""
    if request.method == 'POST':
        text = request.POST.get('todo_text', '').strip()
        if text:
            todos = request.session.get('todos', [])
            next_id = request.session.get('next_id', 1)
            
            new_todo = {'id': next_id, 'text': text, 'completed': False}
            todos.append(new_todo)
            
            request.session['todos'] = todos
            request.session['next_id'] = next_id + 1
            request.session.modified = True
            
            # Return the new todo item HTML and clear the form
            todo_html = render_todo_item(new_todo)
            return HttpResponse(
                f'{todo_html}'
                f'<input type="text" name="todo_text" id="todo-input" placeholder="Add a new task..." '
                f'class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500" '
                f'hx-post="/todos/add/" hx-target="#todo-list" hx-swap="afterbegin" hx-trigger="keyup[key==\'Enter\']" '
                f'hx-on::after-request="this.value=\'\'">'
            )
    return HttpResponse('')


def toggle_todo(request, todo_id):
    """Toggle todo completion status."""
    todos = request.session.get('todos', [])
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            request.session.modified = True
            return HttpResponse(render_todo_item(todo))
    return HttpResponse('')


def edit_todo(request, todo_id):
    """Return edit form for a todo."""
    todos = request.session.get('todos', [])
    for todo in todos:
        if todo['id'] == todo_id:
            return HttpResponse(f'''
                <li id="todo-{todo['id']}" class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                    <input type="text" value="{todo['text']}" 
                        class="flex-1 px-3 py-1 border border-purple-300 rounded focus:outline-none focus:ring-2 focus:ring-purple-500"
                        hx-post="/todos/{todo['id']}/save/"
                        hx-trigger="keyup[key=='Enter']"
                        hx-target="#todo-{todo['id']}"
                        hx-swap="outerHTML"
                        name="todo_text"
                        autofocus>
                    <button class="text-gray-400 hover:text-gray-600"
                        hx-get="/todos/"
                        hx-target="#todo-list"
                        hx-swap="innerHTML">
                        Cancel
                    </button>
                </li>
            ''')
    return HttpResponse('')


def save_todo(request, todo_id):
    """Save edited todo."""
    if request.method == 'POST':
        todos = request.session.get('todos', [])
        new_text = request.POST.get('todo_text', '').strip()
        if new_text:
            for todo in todos:
                if todo['id'] == todo_id:
                    todo['text'] = new_text
                    request.session.modified = True
                    return HttpResponse(render_todo_item(todo))
    return HttpResponse('')


def delete_todo(request, todo_id):
    """Delete a todo with undo option."""
    todos = request.session.get('todos', [])
    deleted_todo = None
    for i, todo in enumerate(todos):
        if todo['id'] == todo_id:
            deleted_todo = todos.pop(i)
            request.session.modified = True
            break
    
    if deleted_todo:
        # Return undo notification
        return HttpResponse(f'''
            <div class="p-3 bg-yellow-100 border border-yellow-400 rounded-lg flex items-center justify-between animate-slide-in">
                <span class="text-yellow-800">Deleted "{deleted_todo['text']}"</span>
                <button class="text-yellow-800 hover:text-yellow-900 font-semibold"
                    hx-post="/todos/undo/"
                    hx-vals='{json.dumps(deleted_todo)}'
                    hx-target="#undo-notification"
                    hx-swap="outerHTML">
                    Undo
                </button>
            </div>
        ''')
    return HttpResponse('')


def undo_delete(request):
    """Restore a deleted todo."""
    if request.method == 'POST':
        todo_data = {
            'id': int(request.POST.get('id')),
            'text': request.POST.get('text'),
            'completed': request.POST.get('completed') == 'True'
        }
        todos = request.session.get('todos', [])
        todos.append(todo_data)
        request.session.modified = True
        
        # Return empty (clear notification) and trigger list refresh
        return HttpResponse('<div hx-get="/todos/" hx-trigger="load" hx-target="#todo-list" hx-swap="innerHTML"></div>')
    return HttpResponse('')


def clear_completed(request):
    """Clear all completed todos."""
    todos = request.session.get('todos', [])
    active_todos = [t for t in todos if not t['completed']]
    request.session['todos'] = active_todos
    request.session.modified = True
    return HttpResponse(render_todo_list(active_todos, 'all'))


# Helper functions

def render_todo_item(todo):
    """Render a single todo item."""
    completed_class = 'line-through text-gray-400' if todo['completed'] else 'text-gray-800'
    checkbox_class = 'checked' if todo['completed'] else ''
    
    return f'''
        <li id="todo-{todo['id']}" class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors group">
            <input type="checkbox" {checkbox_class}
                class="w-5 h-5 text-purple-600 rounded focus:ring-2 focus:ring-purple-500"
                hx-post="/todos/{todo['id']}/toggle/"
                hx-target="#todo-{todo['id']}"
                hx-swap="outerHTML">
            <span class="flex-1 {completed_class}">{todo['text']}</span>
            <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button class="text-blue-500 hover:text-blue-700"
                    hx-get="/todos/{todo['id']}/edit/"
                    hx-target="#todo-{todo['id']}"
                    hx-swap="outerHTML">
                    Edit
                </button>
                <button class="text-red-500 hover:text-red-700"
                    hx-delete="/todos/{todo['id']}/delete/"
                    hx-target="#undo-notification"
                    hx-swap="innerHTML"
                    hx-confirm="Are you sure?">
                    Delete
                </button>
            </div>
        </li>
    '''


def render_todo_list(todos, filter_type='all'):
    """Render the complete todo list."""
    if not todos:
        return '<li class="text-center text-gray-400 py-8">No tasks found. Add one above!</li>'
    
    return ''.join(render_todo_item(todo) for todo in todos)

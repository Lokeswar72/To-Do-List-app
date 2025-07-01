from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TaskForm(instance=task)
    tasks = Task.objects.all()
    return render(request, 'todo/index.html', {
        'form': TaskForm(),
        'tasks': tasks,
        'edit_form': form,
        'edit_id': task_id
    })


def index(request):
    filter_option = request.GET.get('filter', 'all')

    if filter_option == 'completed':
        tasks = Task.objects.filter(completed=True)
    elif filter_option == 'incomplete':
        tasks = Task.objects.filter(completed=False)
    else:
        tasks = Task.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TaskForm()

    return render(request, 'todo/index.html', {
        'tasks': tasks,
        'form': form,
        'filter_option': filter_option,
    })


def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('index')

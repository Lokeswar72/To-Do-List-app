from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.db.models import Case, When
from django.utils import timezone
from django.views.decorators.http import require_POST


@require_POST
def bulk_action(request):
    action = request.POST.get("action")
    selected_ids = request.POST.getlist("selected_tasks")

    if selected_ids:
        tasks = Task.objects.filter(id__in=selected_ids)
        if action == "complete":
            tasks.update(completed=True)
        elif action == "delete":
            tasks.delete()

    return redirect("index")


def annotate_overdue(tasks):
    """Adds `overdue` attribute to each task (used in template rendering)"""
    today = timezone.now().date()
    for task in tasks:
        task.overdue = not task.completed and task.due_date and task.due_date < today
    return tasks


def index(request):
    filter_option = request.GET.get('filter', 'all')
    sort_option = request.GET.get('sort', 'default')

    tasks = Task.objects.all()

    # Apply filter
    if filter_option == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_option == 'incomplete':
        tasks = tasks.filter(completed=False)
    elif filter_option in ['high', 'medium', 'low']:
        tasks = tasks.filter(priority=filter_option)

    # Apply sorting
    if sort_option == 'due':
        tasks = tasks.order_by('due_date')
    elif sort_option == 'priority':
        tasks = tasks.order_by(
            Case(
                When(priority='high', then=0),
                When(priority='medium', then=1),
                When(priority='low', then=2),
            )
        )
    else:
        tasks = tasks.order_by('id')

    # Mark overdue tasks
    tasks = annotate_overdue(tasks)

    # Handle new task form
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
        'sort_option': sort_option,
    })


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TaskForm(instance=task)

    filter_option = request.GET.get('filter', 'all')
    sort_option = request.GET.get('sort', 'default')
    tasks = Task.objects.all()

    # Apply filter
    if filter_option == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_option == 'incomplete':
        tasks = tasks.filter(completed=False)
    elif filter_option in ['high', 'medium', 'low']:
        tasks = tasks.filter(priority=filter_option)

    # Apply sorting
    if sort_option == 'due':
        tasks = tasks.order_by('due_date')
    elif sort_option == 'priority':
        tasks = tasks.order_by(
            Case(
                When(priority='high', then=0),
                When(priority='medium', then=1),
                When(priority='low', then=2),
            )
        )
    else:
        tasks = tasks.order_by('id')

    # Mark overdue tasks
    tasks = annotate_overdue(tasks)

    return render(request, 'todo/index.html', {
        'form': TaskForm(),
        'edit_form': form,
        'tasks': tasks,
        'edit_id': task_id,
        'filter_option': filter_option,
        'sort_option': sort_option,
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

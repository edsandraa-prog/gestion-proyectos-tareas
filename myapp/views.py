
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task
from .forms import ProjectForm, TaskForm


# Página de inicio
def hello(request):

    total_proyectos = Project.objects.count()

    total_tareas = Task.objects.count()

    tareas_terminadas = Task.objects.filter(
        completed=True
    ).count()

    tareas_pendientes = Task.objects.filter(
        completed=False
    ).count()

    return render(request, 'myapp/hello.html', {
        'total_proyectos': total_proyectos,
        'total_tareas': total_tareas,
        'tareas_terminadas': tareas_terminadas,
        'tareas_pendientes': tareas_pendientes,
    })


# Mostrar todos los proyectos
def projects(request):
    projects = Project.objects.all()
    return render(request, 'myapp/projects.html', {
        'projects': projects
    })


# Mostrar detalles de un proyecto
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)

    return render(request, 'myapp/project_detail.html', {
        'project': project,
        'tasks': tasks
    })


# Crear un nuevo proyecto
def create_project(request):
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('projects')

    return render(request, 'myapp/create_project.html', {
        'form': form
    })


# Mostrar todas las tareas
def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'myapp/tasks.html', {
        'tasks': tasks
    })


# Crear una nueva tarea
def create_task(request):
    form = TaskForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('tasks')

    return render(request, 'myapp/create_task.html', {
        'form': form
    })


# Editar una tarea
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    form = TaskForm(request.POST or None, instance=task)

    if form.is_valid():
        form.save()
        return redirect('tasks')

    return render(request, 'myapp/edit_task.html', {
        'form': form,
        'task': task
    })


# Eliminar una tarea
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

    return render(request, 'myapp/delete_task.html', {
        'task': task
    })


# Marcar una tarea como terminada o pendiente
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()

    return redirect('tasks')

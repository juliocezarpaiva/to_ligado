from django.shortcuts import redirect, render, get_object_or_404
from background_task import background
from django.contrib.auth.models import User
from background_task.models import Task, CompletedTask

@background(schedule=60)
def create_task(request, update_interval, higher_limit, lower_limit):
    user = get_object_or_404(User, pk=request.user.id)
    Task.objects.filter(creator=user, locked_at__isnull=True).delete()
    CompletedTask.objects.filter(creator=user, locked_at__isnull=True).delete()
    return redirect('home')

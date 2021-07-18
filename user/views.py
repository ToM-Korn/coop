from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, resolve_url

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required, permission_required

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required()
@permission_required('is_staff')
def users(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users':users})
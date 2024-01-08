from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.models import Group
from django.urls import reverse, reverse_lazy
from users.forms import customUserCreationForm


# Create your views here.
class SignUpView(CreateView):
    model = get_user_model()
    form_class = customUserCreationForm
    template_name = 'users/sign_up.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        # user_type = self.request.POST.get('user_type')
        user_type = form.cleaned_data['user_type']
        # user_type = form['user_type'].value()
        if user_type == 'customer':
            group = Group.objects.get(name='Customer')
        elif user_type == 'employee':
            group = Group.objects.get(name='Employee')

        user.save()
        user.groups.add(group)
        return response

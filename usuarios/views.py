from django.contrib.auth.models import Group
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import AlunoSignupForm, ProfessorSignupForm
from django.contrib.auth.models import User

class AlunoSignupView(CreateView):
    model = User
    form_class = AlunoSignupForm
    template_name = 'usuarios/cadastro_aluno.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        aluno_group, created = Group.objects.get_or_create(name='aluno')
        self.object.groups.add(aluno_group)
        return response


class ProfessorSignupView(CreateView):
    model = User
    form_class = ProfessorSignupForm
    template_name = 'usuarios/cadastro_professor.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        grupo, created = Group.objects.get_or_create(name='professor')
        self.object.groups.add(grupo)
        return response
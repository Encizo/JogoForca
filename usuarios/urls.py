from django.urls import path
from .views import AlunoSignupView, ProfessorSignupView
from django.contrib.auth.views import LoginView, LogoutView

class LogoutGetAllowedView(LogoutView):
    # Permite logout via GET
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

urlpatterns = [
    path('cadastro/', AlunoSignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('cadastro-professor/', ProfessorSignupView.as_view(), name='signup_professor'),
]

from django.urls import path
from .views import IndexView, TemaListView, TemaPalavraCreateView, JogoForcaView, JogoPorTemaView, ExcluirTemaView, ExcluirPalavraView, GerarPDFView, RelatorioView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('temas/', TemaListView.as_view(), name='lista_temas'),
    path('cadastro/', TemaPalavraCreateView.as_view(), name='cadastro_tema_palavra'),
    path('jogo/', JogoForcaView.as_view(), name='jogar'),
    path('jogo/tema/<int:tema_id>/', JogoPorTemaView.as_view(), name='jogar_por_tema'),
    path('excluir/tema/<int:tema_id>/', ExcluirTemaView.as_view(), name='excluir_tema'),
    path('excluir/palavra/<int:palavra_id>/', ExcluirPalavraView.as_view(), name='excluir_palavra'),
    path('professor/pdf/<int:tema_id>/', GerarPDFView.as_view(), name='gerar_pdf'),
    path('professor/relatorio/', RelatorioView.as_view(), name='relatorio'),
]

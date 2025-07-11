from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
import random
from .forms import TemaForm, PalavraForm, RelatorioForm
from .models import Tema, Palavra, Partida
from django.utils.timezone import make_aware
from datetime import datetime
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


class ProfessorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='professor').exists()


class TemaPalavraCreateView(LoginRequiredMixin, ProfessorRequiredMixin, View):
    template_name = 'jogo/tema_palavra_form.html'

    def get(self, request):
        tema_form = TemaForm()
        palavra_form = PalavraForm()
        return render(request, self.template_name, {
            'tema_form': tema_form,
            'palavra_form': palavra_form,
        })

    def post(self, request):
        tema_form = TemaForm(request.POST)
        palavra_form = PalavraForm(request.POST)

        if 'submit_tema' in request.POST:
            if tema_form.is_valid():
                tema = tema_form.save(commit=False)
                tema.criado_por = request.user
                tema.save()
                return redirect('lista_temas')
        elif 'submit_palavra' in request.POST:
            if palavra_form.is_valid():
                palavra_form.save()
                return redirect('lista_temas')

        return render(request, self.template_name, {
            'tema_form': tema_form,
            'palavra_form': palavra_form,
        })


class IndexView(View):
    template_name = 'jogo/index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        tema = Tema.objects.order_by('?').first()
        if not tema:
            return redirect('lista_temas')
        return redirect('jogar_por_tema', tema_id=tema.id)


class TemaListView(ListView):
    model = Tema
    template_name = 'jogo/lista_temas.html'
    context_object_name = 'temas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_professor'] = user.is_authenticated and user.groups.filter(name='professor').exists()
        context['is_anonimo'] = not user.is_authenticated
        return context


class JogoForcaView(View):
    def get(self, request):
        palavra_id = request.session.get('palavra_id')
        if not palavra_id:
            return redirect('lista_temas')

        palavra_obj = Palavra.objects.get(id=palavra_id)
        palavra = palavra_obj.texto.upper()
        letras_certas = request.session.get('letras_certas', [])
        letras_erradas = request.session.get('letras_erradas', [])
        mostrar_dica = request.session.get('mostrar_dica', False)

        return render(request, 'jogo/partida.html', {
            'palavra': palavra,
            'letras_certas': letras_certas,
            'letras_erradas': letras_erradas,
            'erros': len(letras_erradas),
            'ganhou': False,
            'perdeu': False,
            'tema': palavra_obj.tema.nome,
            'dica': palavra_obj.dica,
            'mostrar_dica': mostrar_dica,
        })

    def post(self, request):
        palavra_obj = Palavra.objects.get(id=request.session['palavra_id'])
        palavra = palavra_obj.texto.upper()
        letras_certas = request.session.get('letras_certas', [])
        letras_erradas = request.session.get('letras_erradas', [])
        mostrar_dica = request.session.get('mostrar_dica', False)

        acao = request.POST.get('acao')

        ganhou = False
        perdeu = False

        if acao == 'mostrar_dica':
            request.session['mostrar_dica'] = True
            mostrar_dica = True

        elif acao == 'chutar_palavra':
            palpite = request.POST.get('palpite', '').strip().upper()
            if palpite == palavra:
                ganhou = True
                # Completa todas as letras para mostrar a palavra cheia
                letras_certas = list(set([l for l in palavra if l != ' ']))
                request.session['letras_certas'] = letras_certas
            else:
                perdeu = True

            Partida.objects.create(
                palavra=palavra_obj,
                aluno=request.user if request.user.is_authenticated else None,
                acertou=ganhou,
                tentativas=len(letras_certas) + len(letras_erradas)
            )

            return render(request, 'jogo/partida.html', {
                'palavra': palavra,
                'letras_certas': letras_certas,
                'letras_erradas': letras_erradas,
                'erros': len(letras_erradas),
                'ganhou': ganhou,
                'perdeu': perdeu,
                'tema': palavra_obj.tema.nome,
                'dica': palavra_obj.dica,
                'mostrar_dica': mostrar_dica,
            })

        elif acao == 'tentar_letra':
            letra = request.POST.get('letra', '').strip().upper()
            if letra and letra not in letras_certas and letra not in letras_erradas:
                if letra in palavra:
                    letras_certas.append(letra)
                else:
                    letras_erradas.append(letra)

        request.session['letras_certas'] = letras_certas
        request.session['letras_erradas'] = letras_erradas

        ganhou = all(l in letras_certas or l == " " for l in palavra)
        perdeu = len(letras_erradas) >= 6

        if ganhou or perdeu:
            Partida.objects.create(
                palavra=palavra_obj,
                aluno=request.user if request.user.is_authenticated else None,
                acertou=ganhou,
                tentativas=len(letras_certas) + len(letras_erradas)
            )

        return render(request, 'jogo/partida.html', {
            'palavra': palavra,
            'letras_certas': letras_certas,
            'letras_erradas': letras_erradas,
            'erros': len(letras_erradas),
            'ganhou': ganhou,
            'perdeu': perdeu,
            'tema': palavra_obj.tema.nome,
            'dica': palavra_obj.dica,
            'mostrar_dica': mostrar_dica,
        })


class JogoPorTemaView(View):
    def get(self, request, tema_id):
        tema = get_object_or_404(Tema, id=tema_id)
        palavras = tema.palavras.all()

        if not palavras.exists():
            return redirect('lista_temas')

        palavra = random.choice(list(palavras))
        request.session['palavra_id'] = palavra.id
        request.session['letras_certas'] = []
        request.session['letras_erradas'] = []
        request.session['mostrar_dica'] = False
        request.session['anonimo'] = request.GET.get('anonimo') == '1'

        return redirect('jogar')

class ExcluirTemaView(LoginRequiredMixin, View):
    def post(self, request, tema_id):
        tema = get_object_or_404(Tema, id=tema_id)

        # Somente o professor que criou pode excluir
        if tema.criado_por != request.user:
            return HttpResponseForbidden("Você não tem permissão para excluir este tema.")

        tema.delete()
        return redirect('lista_temas')


class ExcluirPalavraView(LoginRequiredMixin, View):
    def post(self, request, palavra_id):
        palavra = get_object_or_404(Palavra, id=palavra_id)

        # Verifica se o usuário é o criador do tema relacionado
        if palavra.tema.criado_por != request.user:
            return HttpResponseForbidden("Você não tem permissão para excluir esta palavra.")

        palavra.delete()
        return redirect('lista_temas')

class GerarPDFView(LoginRequiredMixin, ProfessorRequiredMixin, View):
    def get(self, request, tema_id):
        try:
            tema = Tema.objects.get(id=tema_id, criado_por=request.user)
        except Tema.DoesNotExist:
            return HttpResponseForbidden("Você não tem permissão para gerar PDF desse tema.")

        palavras = tema.palavras.all()
        template = get_template('jogo/pdf_tema.html')
        html = template.render({'tema': tema, 'palavras': palavras})

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="atividade_{tema.nome}.pdf"'

        pisa.CreatePDF(html, dest=response)
        return response


class RelatorioView(LoginRequiredMixin, ProfessorRequiredMixin, View):
    def get(self, request):
        tema_id = request.GET.get('tema')
        tema = get_object_or_404(Tema, id=tema_id, criado_por=request.user)

        # Carrega todas as partidas do tema ao entrar
        partidas = Partida.objects.filter(
            palavra__tema=tema
        ).select_related('aluno', 'palavra', 'palavra__tema')

        form = RelatorioForm()

        return render(request, 'jogo/relatorio.html', {
            'form': form,
            'partidas': partidas,
            'tema': tema,
        })

    def post(self, request):
        tema_id = request.GET.get('tema')
        tema = get_object_or_404(Tema, id=tema_id, criado_por=request.user)

        form = RelatorioForm(request.POST)
        partidas = Partida.objects.filter(
            palavra__tema=tema
        ).select_related('aluno', 'palavra', 'palavra__tema')

        if form.is_valid():
            data_inicio = form.cleaned_data.get('data_inicio')
            data_fim = form.cleaned_data.get('data_fim')

            if data_inicio:
                partidas = partidas.filter(
                    data__gte=make_aware(datetime.combine(data_inicio, datetime.min.time()))
                )
            if data_fim:
                partidas = partidas.filter(
                    data__lte=make_aware(datetime.combine(data_fim, datetime.max.time()))
                )

        return render(request, 'jogo/relatorio.html', {
            'form': form,
            'partidas': partidas,
            'tema': tema,
        })
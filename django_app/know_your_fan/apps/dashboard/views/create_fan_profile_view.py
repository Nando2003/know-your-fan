from celery import chain
from django.db import transaction
from django.views.generic import View
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from apps.dashboard.models.dashboard_model import Dashboard
from apps.dashboard.models.fan_profile_model import FanProfile

from apps.dashboard.forms.create_fan_profile_form import (
    CreateFanProfileForm, FanEventFormSet, PurchaseFormSet
)

from apps.dashboard.tasks.recommend_news_for_dashboard_task import recommend_news_for_dashboard
from apps.dashboard.tasks.twitter_scores_scraping_task import update_dashboard_twitter

@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class CreateFanProfileView(View):
    template_name = 'dashboard/create_fan_profile.html'

    def get(self, request):
        # Instância em branco já vinculada ao user_info
        profile = FanProfile(user_info=request.user.userinfo)

        form = CreateFanProfileForm(instance=profile)
        events_fs = FanEventFormSet(instance=profile, prefix='events')
        purchases_fs = PurchaseFormSet(instance=profile, prefix='purchases')

        # Checa tokens do Twitter na sessão
        access_token = request.session.pop('twitter_oauth2_access_token', None)
        twitter_logged_in = bool(access_token)

        # Monta contexto
        context = {
            'form': form,
            'events_fs': events_fs,
            'purchases_fs': purchases_fs,
            'twitter_logged_in': twitter_logged_in
        }

        if twitter_logged_in:
            context['twitter_tokens'] = {
            'access_token': access_token,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = CreateFanProfileForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'events_fs': FanEventFormSet(prefix='events'),
                'purchases_fs': PurchaseFormSet(prefix='purchases'),
            })

        access_token = request.POST.get('twitter_access_token')

        try:
            with transaction.atomic():
                # salva perfil
                profile: FanProfile = form.save(commit=False)
                profile.user_info = request.user.userinfo
                profile.save()
                form.save_m2m()

                # cria e valida formsets sobre o perfil já salvo
                events_fs = FanEventFormSet(request.POST, instance=profile, prefix='events')
                purchases_fs = PurchaseFormSet(request.POST, instance=profile, prefix='purchases')
                
                if not events_fs.is_valid() or not purchases_fs.is_valid():
                    raise ValueError("Formset inválido")

                # salva os itens em loop
                events_fs.save()
                purchases_fs.save()

                # cria dashboard
                dash = Dashboard.objects.create(fan_profile=profile)

                chain(
                    recommend_news_for_dashboard.s(dash.id), # type: ignore
                    update_dashboard_twitter.s(dash.id, access_token), # type: ignore
                ).apply_async()

        except ValueError as e:
            print(f"Erro ao criar o perfil: {e}")
            # rollback automático pelo atomic()
            return render(request, self.template_name, {
                'form': form,
                'events_fs': events_fs, # type: ignore
                'purchases_fs': purchases_fs, # type: ignore
                'error_message': 'Formulário de eventos ou compras inválido.'
            })
            
        except Exception as e:
            print(f"Erro ao criar o perfil: {e}")
            return render(request, self.template_name, {
                'form': form,
                'events_fs': events_fs, # type: ignore
                'purchases_fs': purchases_fs, # type: ignore
                'error_message': 'Erro ao salvar os dados. Tente novamente.'
            })

        return redirect('dashboard:dashboard_list')

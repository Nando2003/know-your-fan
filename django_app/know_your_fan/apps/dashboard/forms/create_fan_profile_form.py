from django import forms
from apps.dashboard.models.game_model import Game
from apps.dashboard.models.team_model import Team
from apps.dashboard.models.purchase_model import Purchase
from apps.dashboard.models.fan_event_model import FanEvent
from apps.dashboard.models.fan_profile_model import FanProfile

    
class CreateFanProfileForm(forms.ModelForm):
    
    org_preference = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.Select(),
        required=True,
        label="Organização Favorita"
    )
    
    games = forms.ModelMultipleChoiceField(
        queryset=Game.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label="Jogos de Interesse"
    )
    
    class Meta:
        model = FanProfile
        fields = ['org_preference', 'games']
    
    def clean_games(self):
        check_games = self.cleaned_data.get('games')
        if not check_games or len(check_games) == 0:
            raise forms.ValidationError("Selecione ao menos um jogo de interesse.")
        return check_games


# 1) Cria um ModelForm para o evento
class FanEventForm(forms.ModelForm):
    date = forms.DateField(
        label="Data do Evento (mês/ano)",
        widget=forms.DateInput(attrs={'type': 'month'}),
        input_formats=['%Y-%m'],
    )

    class Meta:
        model = FanEvent
        fields = ['date', 'event_type', 'description']

    def clean_date(self):
        dt = self.cleaned_data['date']
        return dt.replace(day=1)


# 2) Cria um ModelForm para a compra
class PurchaseForm(forms.ModelForm):
    date = forms.DateField(
        label="Data da Compra (mês/ano)",
        widget=forms.DateInput(attrs={'type': 'month'}),
        input_formats=['%Y-%m'],
    )

    class Meta:
        model = Purchase
        fields = ['date', 'item', 'cost']

    def clean_date(self):
        dt = self.cleaned_data['date']
        return dt.replace(day=1)


FanEventFormSet = forms.inlineformset_factory(
    parent_model=FanProfile,
    model=FanEvent,
    form=FanEventForm,
    extra=1,
    can_delete=False,
    max_num=8,
    validate_max=True,
)

PurchaseFormSet = forms.inlineformset_factory(
    parent_model=FanProfile,
    model=Purchase,
    form=PurchaseForm,
    extra=1,
    can_delete=False,
    max_num=8,
    validate_max=True,
)


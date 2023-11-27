from datetime import date

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import PromoCode, TicketKind, User


class SignupForm(forms.Form):
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    email = forms.EmailField()
    status = forms.CharField(disabled=True)


class NameChangeForm(forms.Form):
    new_name = forms.CharField(max_length=100, initial="")
    new_email = forms.EmailField(initial="")


class BuyTicketForm(forms.Form):
    def __init__(self, tickets_qs, *args, **kwargs):
        super(BuyTicketForm, self).__init__(*args, **kwargs)
        self.fields['kind'].queryset = tickets_qs
        for kind in tickets_qs:
            for extra in kind.optional_extras.all():
                self.fields[f'{extra.enum.lower()}_{kind.pk}'] = forms.BooleanField(
                    initial=extra.opt_out,
                    label=extra.label,
                    required=False,
                )

    full_name = forms.CharField(max_length=100, initial="")
    email = forms.EmailField(initial="")
    kind = forms.ModelChoiceField(queryset=None, initial=1)
    is_alc = forms.BooleanField(required=False)
    is_veg = forms.BooleanField(required=False)
    is_ubus = forms.BooleanField(required=False)
    is_departure_bus = forms.BooleanField(required=False)
    # Probably shouldn't hardcode this lol
    bus_destination_choices = [
        ('unselected', 'Optional'),
        ('station', 'Cambridge Train Station'),
        ('city_centre', 'Cambridge City Centre'),
        ('swirles', 'Swirles Court'),
    ]
    bus_destination = forms.ChoiceField(choices=bus_destination_choices)

    verif = forms.CharField(max_length=100, initial="", required=False)

    def clean_verif(self):
        data = self.cleaned_data['verif']
        alum_code = PromoCode.objects.get(enum='ALUM_SIGNUP')
        #bursary_code = PromoCode.objects.get(enum='BURSARY_ENABLE')
        kind = self.cleaned_data.get('kind')
        print(kind)
        if data == alum_code.value:
            raise ValidationError(
                "You are logged in with a Raven account! Please logout and use the Alumni sign in option."
            )
        """
        elif (
            kind
            and data != bursary_code.value
            and (kind.enum == "S_BURSARY" or kind.enum == "QJ_BURSARY")
        ):
            print(self.cleaned_data['kind'])
            raise ValidationError("Invalid code for Bursary ticket!")
        """
        return data


class WorkerApplicationForm(forms.Form):
    def __init__(self, worker_roles_qs, *args, **kwargs):
        super(WorkerApplicationForm, self).__init__(*args, **kwargs)
        self.fields['choice1'].queryset = worker_roles_qs
        self.fields['choice2'].queryset = worker_roles_qs

    # Probably shouldn't hardcode this either
    colleges = [
        ("christs", "Christ's College"),
        ("churchill", "Churchill College"),
        ("clare", "Clare College"),
        ("clarehall", "Clare Hall"),
        ("corpuschristi", "Corpus Christi College"),
        ("darwin", "Darwin College"),
        ("downing", "Downing College"),
        ("emmanuel", "Emmanuel College"),
        ("fitzwilliam", "Fitzwilliam College"),
        ("girton", "Girton College"),
        ("cauis", "Gonville & Caius College"),
        ("hometon", "Homerton College"),
        ("hugheshall", "Hughes Hall"),
        ("jesus", "Jesus College"),
        ("kings", "King's College"),
        ("lucycavendish", "Lucy Cavendish College"),
        ("magdalene", "Magdalene College"),
        ("murrayedwards", "Murray Edwards College"),
        ("newnham", "Newnham College"),
        ("pembroke", "Pembroke College"),
        ("peterhouse", "Peterhouse"),
        ("queens", "Queens' College"),
        ("robinson", "Robinson College"),
        ("selwyn", "Selwyn College"),
        ("sidneysussex", "Sidney Sussex College"),
        ("stcatherines", "St Catharine's College"),
        ("stedmunds", "St Edmund's College"),
        ("stjohns", "St John's College"),
        ("trinity", "Trinity College"),
        ("trinityhall", "Trinity Hall"),
        ("wolfson", "Wolfson College"),
    ]
    name = forms.CharField(max_length=100, initial="")
    crsid = forms.CharField(max_length=8, initial="")
    dob = forms.DateField()
    college = forms.ChoiceField(choices=colleges)
    choice1 = forms.ModelChoiceField(queryset=None, initial=1)
    choice2 = forms.ModelChoiceField(queryset=None, initial=1)
    supervisor = forms.BooleanField(required=False)
    reason = forms.CharField(initial="")
    previous_exp = forms.BooleanField(required=False)
    exp_desc = forms.CharField(initial="")
    other_exp = forms.CharField(initial="")
    qualities = forms.CharField(initial="")
    friends = forms.CharField(initial="")


class GuestLoginForm(forms.Form):
    email = forms.EmailField()
    passphrase = forms.CharField(max_length=30)


class GuestSignupForm(forms.Form):
    name = forms.CharField(max_length=100, initial="")
    surname = forms.CharField(max_length=100, initial="")
    email = forms.EmailField(initial="")
    passphrase = forms.CharField(min_length=14)
    matric_date = forms.DateField()
    pname = forms.CharField(max_length=100, required=False, initial="")
    psurname = forms.CharField(max_length=100, required=False, initial="")
    promocode = forms.CharField(max_length=30)

    def clean_promocode(self):
        data = self.cleaned_data['promocode']
        # 500 if no code defined
        alum_code = PromoCode.objects.get(enum='ALUM_SIGNUP')
        if data != alum_code.value:
            raise ValidationError("Incorrect alumni verification code")

        return data

    def clean_password(self):
        data = self.cleaned_data['passphrase']
        validate_password(data)
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        # check valid username
        if User.objects.filter(username=data).exists():
            raise ValidationError("A user with that email already exists!")

        return data

from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *


class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        exclude = ()

ChoiceFormSet = inlineformset_factory(
    Question, Choice, form=ChoiceForm,
    fields=['choice_text'], extra=1, can_delete=True
    )


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('question_text'),
                Fieldset('Add choices',
                    Formset('choices')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Save')),
                )
            )
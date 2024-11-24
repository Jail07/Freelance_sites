from django import forms
from .models import Project, Review


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Добавляем классы для всех полей
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # Дополнительные настройки для полей
        self.fields['description'].widget.attrs.update(
            {'placeholder': 'Describe your project here...', 'maxlength': '500'})
        self.fields['title'].widget.attrs.update(
            {'placeholder': 'Enter project title', 'maxlength': '200'})

    def clean_title(self):
        # Проверка на уникальность названия проекта
        title = self.cleaned_data.get('title')
        if Project.objects.filter(title=title).exists():
            raise forms.ValidationError('A project with this title already exists.')
        return title


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        # Добавляем классы для всех полей
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # Дополнительные настройки для полей
        self.fields['body'].widget.attrs.update(
            {'placeholder': 'Add a comment...', 'maxlength': '500'})

    def clean_body(self):
        # Пример простой проверки на длину комментария
        body = self.cleaned_data.get('body')
        if len(body) < 10:
            raise forms.ValidationError('Comment must be at least 10 characters long.')
        return body

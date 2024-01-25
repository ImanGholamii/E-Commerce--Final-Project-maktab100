from django import forms


class EmailForm(forms.Form):
    recipient = forms.EmailField()
    subject = forms.CharField(max_length=256)
    message = forms.CharField(widget=forms.Textarea)
    template_name = 'email_form.html'

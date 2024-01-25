from django.shortcuts import render

# Create your views here.
def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(
                subject,
                message,
                'sharlotimi@gmail.com',
                [recipient],
                fail_silently=False,
            )
            # return render(request, 'success.html')
            return HttpResponse('Done')
    else:
        form = EmailForm()
    return render(request, 'email_sender/email_form.html', {'form': form})
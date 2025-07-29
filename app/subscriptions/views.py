from django.shortcuts import render

def index(request):
    context = {
        'page_title': 'Dashboard',
    }
    return render(request, 'subscriptions/dashboard.html', context)

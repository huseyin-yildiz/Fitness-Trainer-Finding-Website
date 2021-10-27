from django.shortcuts import render, HttpResponse

context = {
    'isim': 'Barış',
}

def home_view(request):
    if request.user.is_authenticated:
        context = {
            'isim': 'Aygün',
        }
    else:
        context = {
            'isim': 'Misafir',
        }
    return render(request, 'home.html', context)

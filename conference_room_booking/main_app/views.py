from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render


def main_page_view(request):
    return render(request, 'home_page.html')

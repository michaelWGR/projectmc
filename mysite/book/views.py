# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response,render

from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.core.mail import send_mail
import datetime
from .models import Book
from .forms import ContactForm

def current_datetime(request):
    # now = datetime.datetime.now()
    current_date = datetime.datetime.now()
    return render_to_response('book/current_datetime.html', locals())
    # return render(request, 'book/current_datetime.html', {'current_date': now })
    # return HttpResponse(now)

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404
    current_time = datetime.datetime.now()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>{}</br>In {} hour(s),it will be {}</body></html>".format(current_time,offset,dt)
    return HttpResponse(html)

def mypage(request):
    page_title = 'This is my page'
    return render_to_response('book/mypage.html', {'title': page_title})
# if __name__ == '__main__':
#     now = datetime.datetime.now()
#     print now

def search_form(request):

    if request.GET['q']:
        parameter = request.GET['q']
        # messqge = 'You are searching for {}'.format(request.GET['q'])
        q = request.GET['q']
        books = Book.objects.filter(title__icontains=q)

        return render_to_response('book/search_form.html', {'parameter': parameter, 'books': books,})
    else:
        if 'q' in request.GET:
            message = 'You submitted an empty form.'
            return HttpResponse(message)

def search(request):
    if 'q' in request.GET and request.GET['q']:
        parameter = request.GET['q']
        # messqge = 'You are searching for {}'.format(request.GET['q'])
        q = request.GET['q']
        books = Book.objects.filter(title__icontains=q)

        return render_to_response('book/search.html', {'parameter': parameter, 'books': books, 'erro': True,})
    else:
        return render_to_response('book/search.html', {'erro': False})


# def contact(request):
#     errors = []
#     if request.method == 'POST':
#         if not request.POST.get('subject', ''):
#             errors.append('Enter a subject.')
#         if not request.POST.get('message', ''):
#             errors.append('Enter a message.')
#         if request.POST.get('email') and '@' not in request.POST.get['email']:
#             errors.append('Enter a valid e-mail address.')
#         if not errors:
#             send_mail(
#                 request.POST['subject'],
#                 request.POST['message'],
#                 request.POST.get('email', 'noreplay@example.com'),
#                 ['siteowner@example.com'],
#             )
#             return HttpResponseRedirect('book/contact_form.html')
#     return render_to_response('book/contact_form.html', {'errors': errors})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreplay@example.com'),
                ['siteowner@example.com'],
            )
            return HttpResponseRedirect('/contact/thanks')
    else:
        form = ContactForm(
            initial={'subject': 'I love your site!'}
        )
    return render_to_response('book/contact_form.html', {'form': form })



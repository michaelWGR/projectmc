# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    string = u'Nothing is impossible.'
    type_list = ['css','java','python']
    info_dict = {'music': u'第一天', 'singer': u'somebody'}

    num_list = map(str,range(100))
    return render(request,'home.html',{'dict': info_dict, 'num_list': ''})
    # return HttpResponse(u'this is michael\'s work')

def secret(request,name):
    person = ['lily','jack','michael','min','rose','1']
    result = ''
    # name = 'michael'
    # name = str(name)
    if name in person:
        result = u'You got my secret.'
    else:
        result = u'sorry,you can try again.'
    return HttpResponse(result)

def secret2(request):
    name = request.GET['a']
    person = ['lily','jack','michael','min','rose','1']
    result = ''
    # name = 'michael'
    # name = str(name)
    if name in person:
        result = u'You got my secret.'
    else:
        result = u'sorry,you can try again.'
    return HttpResponse(result)

def index_redirect(request):
    new_index = reverse('index')
    return HttpResponseRedirect(new_index)
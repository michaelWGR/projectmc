# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django import forms

__author__ = 'LibX'


class PaginatorForm(forms.Form):
    page_num = forms.IntegerField(required=False)
    page_size = forms.IntegerField(required=False)

    def clean_page_num(self):
        value = self.cleaned_data['page_num']
        if value is None:
            return 1
        return value

    def clean_page_size(self):
        value = self.cleaned_data['page_size']
        if value is None:
            return 20
        return value


class SuiteStartForm(forms.Form):
    suite_id = forms.IntegerField()
    start_date = forms.DateField(input_formats=['%Y-%m-%d'])
    end_date = forms.DateField(input_formats=['%Y-%m-%d'])
    case_count = forms.IntegerField(required=False)

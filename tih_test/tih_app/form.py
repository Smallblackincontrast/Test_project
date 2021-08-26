#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/9/2 15:54
# @Author : Ruanzhe
# @File : form.py
# @Software: PyCharm

from django import forms


class BurnInSearchForm(forms.Form):
    start_date = forms.CharField(label="开始日期")
    end_date = forms.CharField(label="结束日期")
    state = forms.CharField(label='状态')

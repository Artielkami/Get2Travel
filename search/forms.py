from django import forms


class Search(forms.Form):
    departure = forms.CharField(max_length=3)
    arrival = forms.CharField(max_length=3)
    way = forms.IntegerField(min_value=1, max_value=2)
    stop = forms.IntegerField(min_value=0, max_value=3)
    go_date = forms.DateField(input_formats='%Y/%m/%d')
    rl_date = forms.DateField(input_formats='%Y/%m/%d')
    adult = forms.IntegerField(min_value=1, max_value=14)
    child = forms.IntegerField(min_value=0, max_value=7)
    babe = forms.IntegerField(min_value=0, max_value=4)


from django import forms


class Search(forms.Form):
    departure = forms.CharField(max_length=3)
    arrival = forms.CharField(max_length=3)
    way = forms.IntegerField(min_value=1, max_value=2)
    stops = forms.IntegerField(min_value=0, max_value=3)
    go_day = forms.DateField()
    rt_day = forms.DateField()
    adult = forms.IntegerField(min_value=1, max_value=14)
    child = forms.IntegerField(min_value=0, max_value=7)
    babe = forms.IntegerField(min_value=0, max_value=4)


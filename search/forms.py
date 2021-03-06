from django import forms


class Search(forms.Form):

    departure = forms.CharField(max_length=3)
    arrival = forms.CharField(max_length=3)
    way = forms.IntegerField(min_value=1, max_value=2)
    stops = forms.IntegerField(min_value=0, max_value=3)
    go_day = forms.DateField()
    rt_day = forms.DateField()
    ttype = forms.CharField(max_length=10)
    adult = forms.IntegerField(min_value=1, max_value=14)
    child = forms.IntegerField(min_value=0, max_value=7)
    babe = forms.IntegerField(min_value=0, max_value=4)

    outhours = forms.CharField(max_length=10)
    inhours = forms.CharField(max_length=10)
    maxprice = forms.CharField(max_length=20)

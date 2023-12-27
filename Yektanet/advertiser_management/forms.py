from django import forms


class AdForm(forms.Form):
    advertiser_id = forms.IntegerField(label="Advertiser ID")
    img_url = forms.ImageField(label="Image")
    title = forms.CharField(label="Title")
    link = forms.CharField(label="URL")

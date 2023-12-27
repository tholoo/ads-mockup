from django import forms


class AdForm(forms.Form):
    advertiser_id = forms.IntegerField(label="Advertiser ID")
    img_url = forms.ImageField(label="Image", max_length=200)
    title = forms.CharField(label="Title", max_length=200)
    link = forms.CharField(label="URL", max_length=200)

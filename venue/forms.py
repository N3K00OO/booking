from django import forms
from venue.models import Category, City, Venue

class VenueForm(forms.ModelForm):
    city = forms.CharField()
    category = forms.CharField()

    class Meta:
        model = Venue
        fields = [
            'name', 'price', 'city', 'category', 'type', 
            'address', 'description', 'image_url'
        ]

    def clean_city(self):
        city_name = self.cleaned_data.get('city')
        try:
            return City.objects.get(name=city_name)
        except City.DoesNotExist:
            raise forms.ValidationError(f"City '{city_name}' does not exist.")

    def clean_category(self):
        category_name = self.cleaned_data.get('category')
        try:
            return Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise forms.ValidationError(f"Category '{category_name}' does not exist.")
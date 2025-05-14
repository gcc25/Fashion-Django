from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control quantity-input',
            'value': 1
        })
    )
    size = forms.CharField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    color = forms.CharField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        
        if product:
            # Dynamically set choices for size
            size_choices = [(size.name, size.name) for size in product.sizes.filter(available=True)]
            if size_choices:
                self.fields['size'].widget.choices = [('', 'Select Size')] + size_choices
            else:
                self.fields['size'].widget = forms.HiddenInput()
            
            # Dynamically set choices for color
            color_choices = [(color.name, color.name) for color in product.colors.filter(available=True)]
            if color_choices:
                self.fields['color'].widget.choices = [('', 'Select Color')] + color_choices
            else:
                self.fields['color'].widget = forms.HiddenInput()
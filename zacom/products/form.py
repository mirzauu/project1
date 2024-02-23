from django.forms import ModelForm
from .models import Product,Product_Variant,Additional_Product_Image,Category
from django import forms



# Product create #


class CreateProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['product_slug','is_active']



class CreateProductVariantForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['is_active'].widget.attrs['class'] = ''
        

    class Meta:
        model = Product_Variant
        fields = '__all__'
        exclude = ['product','product_variant_slug','atributes','additional_images']


        
class EditProductForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['is_active'].widget.attrs['class'] = ''
        

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['product_slug',]
        
        
        
class EditProductVariantForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        
    class Meta:
        model = Product_Variant
        fields = '__all__'
        exclude = ['product_variant_slug']
        

class AddProductVariantForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['is_active'].widget.attrs['class'] = ''
        

    class Meta:
        model = Product_Variant
        fields = '__all__'
        exclude = ['product_variant_slug','atributes','additional_images']        




from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image_field', 'cropping', 'cropping_free')
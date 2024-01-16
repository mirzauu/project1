from django import forms
from customers.models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password'
    }))
  
    class Meta:
        model=Account
        fields = ['first_name','last_name','phone_number','email','password']

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']= 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder']= 'Enter last name'
        self.fields['phone_number'].widget.attrs['placeholder']= 'Enter phone number'   
        self.fields['email'].widget.attrs['placeholder']= 'Enter email'      
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'formbox'    

    def clean(self):
        cleaned_data= super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'password not match'
            )     
        
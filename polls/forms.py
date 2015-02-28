from django import forms
class ContactForm(forms.Form):

    name=forms.CharField(max_length=100)
    gender=forms.CharField()
    university=forms.EmailField()
    graduate=forms.BooleanField(required=False)
    mugshot=forms.ImageField()
    
 
class ContactFormWithMugshot(ContactForm):
	"""docstring for ContactFormWithMugshot"""
	
    
		
		


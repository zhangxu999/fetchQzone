from django import forms
class ContactForm(forms.Form):

    desc=forms.CharField(max_length=100)
    
    image=forms.ImageField()
    
 
class ContactFormWithMugshot(ContactForm):
	"""docstring for ContactFormWithMugshot"""
	
    
		
		


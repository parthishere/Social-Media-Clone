from .models import Post
from django import forms

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('image', 'caption')
        
        def __init__(self, *args,**kwargs):
            # user_set = kwargs.pop('user_set', None)
            # super(TodoModelForm, self).__init__(*args,**kwargs)
            # self.fields['tags'].queryset = Tag.objects.filter(user=user_set)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'
    
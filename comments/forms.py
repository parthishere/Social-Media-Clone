from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = '__all__'
        
        def __init__(self, *args,**kwargs):
            # user_set = kwargs.pop('user_set', None)
            # super(TodoModelForm, self).__init__(*args,**kwargs)
            # self.fields['tags'].queryset = Tag.objects.filter(user=user_set)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'
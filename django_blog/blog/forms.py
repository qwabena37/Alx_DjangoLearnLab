from django import forms
from .models import Post
from .models import Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows':3, 'placeholder':'Write a comment...'}),
        max_length=2000,
        label=''
    )

    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        data = self.cleaned_data['content'].strip()
        if not data:
            raise forms.ValidationError("Comment cannot be empty.")
        return data
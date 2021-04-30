from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')

class CommentForm(forms.Form):
    commentor = forms.CharField(max_length=20)
    comment_text = forms.CharField(widget=forms.Textarea)

    def __str__(self):
        return f"{self.comment_text} by {self.commentor}"

class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=2)
    search_in = forms.ChoiceField(choices=[("title", "Title"),("text","Text"),("tag", "Tag")], required=False)

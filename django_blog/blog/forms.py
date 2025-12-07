from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Tag


# ------------------------------------
# TAG WIDGET (ADDED)
# ------------------------------------
class TagWidget(forms.TextInput):
    """
    A simple widget for entering tags as comma-separated text.
    """
    def __init__(self, attrs=None):
        base_attrs = {
            'class': 'form-control',
            'placeholder': 'Add tags separated by commas (e.g. django, python)',
        }
        if attrs:
            base_attrs.update(attrs)
        super().__init__(attrs=base_attrs)


# ------------------------------------
# USER REGISTRATION
# ------------------------------------
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# ------------------------------------
# USER UPDATE FORMS
# ------------------------------------
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']


# ------------------------------------
# POST FORM (WITH TAG SUPPORT)
# ------------------------------------
class PostForm(forms.ModelForm):

    tags = forms.CharField(
        required=False,
        widget=TagWidget(),   # <--- FIXED: Now using TagWidget
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 5
            }),
        }

    def save(self, commit=True):
        post = super().save(commit=False)

        if commit:
            post.save()

        tag_input = self.cleaned_data.get('tags', '')
        tag_names = [t.strip().lower() for t in tag_input.split(',') if t.strip()]

        # reset old tags
        post.tags.clear()

        # add new tags
        for name in tag_names:
            tag_obj, created = Tag.objects.get_or_create(name=name)
            post.tags.add(tag_obj)

        return post

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            existing_tags = ", ".join([tag.name for tag in self.instance.tags.all()])
            self.fields['tags'].initial = existing_tags


# ------------------------------------
# COMMENT FORM
# ------------------------------------
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Add a comment...',
        }),
        max_length=2000,
        label='',
    )

    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = (self.cleaned_data.get("content") or "").strip()

        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        if len(content) < 2:
            raise forms.ValidationError("Comment is too short.")

        return content

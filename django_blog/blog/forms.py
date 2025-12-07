from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Tag


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

    # Comma-separated tag input
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Add tags separated by commas (e.g. django, python)',
        })
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

    def __init__(self, *args, **kwargs):
        """Pre-fill tag field when editing an existing post."""
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            existing = ", ".join([tag.name for tag in self.instance.tags.all()])
            self.fields['tags'].initial = existing

    def save(self, commit=True):
        """Override save() to process tag input."""
        post = super().save(commit=False)

        if commit:
            post.save()

        # ---- Process tags ----
        raw_tags = self.cleaned_data.get("tags", "")
        tag_names = [
            t.strip().lower()
            for t in raw_tags.split(",")
            if t.strip()
        ]

        # Clear and rebuild tag list
        post.tags.clear()

        for name in tag_names:
            tag_obj, created = Tag.objects.get_or_create(name=name)
            post.tags.add(tag_obj)

        return post


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

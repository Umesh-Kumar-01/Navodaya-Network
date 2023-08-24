from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from mysite.constants import JNV_MAP_LIST, STATES
from .models import UserCard,UserPrivateInfo

class SignUpForm(forms.Form):
    # UserCard fields
    first_name = forms.CharField(max_length=30, help_text='first name',required=True)
    last_name = forms.CharField(max_length=60, help_text='Last name',required=True)
    region_name = forms.ChoiceField(choices=UserCard.RegionName.choices,required=True)
    jnv_name = forms.ChoiceField(choices=[(w,"Jawahar Navodaya Vidyalaya, "+w) for y in JNV_MAP_LIST.values() for w in y],required=True)
    role = forms.ChoiceField(choices=UserCard.ROLE_CHOICES,required=True)
    year = forms.IntegerField(required=False)

    # UserPrivateInfo fields
    user_email = forms.EmailField(required=True)
    profession = forms.CharField(max_length=60, required=False)
    current_location_city = forms.CharField(max_length=300,required=False)
    current_location_state = forms.ChoiceField(choices =[(x,x) for x in STATES],required=False)
    current_location_zip = forms.IntegerField(required=False)

    # User login information
    username = forms.CharField(max_length=150,required=True)
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        required=True
    )
    
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username is already taken.')
        return username

    def clean_user_email(self):
        user_email = self.cleaned_data['user_email']
        if User.objects.filter(email=user_email).exists():
            raise forms.ValidationError('This Email is already Exists.')
        return user_email
    
    def save(self):
        # Create a new User object
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['user_email'],
        )

        # Create UserCard instance
        UserCard.objects.create(
            user=user,
            region_name=self.cleaned_data['region_name'],
            jnv_name=self.cleaned_data['jnv_name'],
            role=self.cleaned_data['role'],
            year=self.cleaned_data['year'],
        )

        # Create UserPrivateInfo instance
        UserPrivateInfo.objects.create(
            user=user,
            current_location_city = self.cleaned_data['current_location_city'],
            current_location_state = self.cleaned_data['current_location_state'],
            current_location_zip =self.cleaned_data['current_location_zip'],
            profession=self.cleaned_data['profession']
        )
        
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserCard
        fields = ['profile_photo']
    
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_photo'].required = False  # Profile photo is optional

class EditPrivateInfoForm(forms.ModelForm):
    class Meta:
        model = UserPrivateInfo
        fields = ['current_location_city', 'current_location_state', 'current_location_zip', 'profession']
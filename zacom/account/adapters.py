
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        # Check if the user signed up via Google
        if sociallogin.account.provider == 'google':
            # Here you can prompt the user to set up a password
            # or ask for additional information.
            # For example:
            user.set_password('')  # Prompt the user to set a password
            user.save()
        return user
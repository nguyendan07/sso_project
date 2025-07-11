from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    """
    Custom OIDC Authentication Backend to handle user creation and filtering
    based on email claims from the OIDC provider.
    """

    def get_email(self, claims):
        email = claims.get("email")
        if not email:
            email = claims.get("sub")
        return email

    def filter_users_by_claims(self, claims):
        """Create user with email base custom user model."""
        email = self.get_email(claims)
        if not email:
            return self.UserModel.objects.none()
        try:
            return self.UserModel.objects.filter(email=email)
        except self.UserModel.DoesNotExist:
            return self.UserModel.objects.none()

    def create_user(self, claims):
        """Create user with email base custom user model."""
        email = self.get_email(claims)
        username = claims.get("nickname")
        if email and not username:
            username = email.split("@")[0]
        user = self.UserModel.objects.create_user(email=email.lower(), username=username.lower())

        return self.update_user(user, claims)

    def update_user(self, user, claims):
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")

        user.save()

        return user

from django import forms


class OIDCConfigForm(forms.Form):
    """Form for OIDC configuration settings"""

    # Basic OIDC Settings
    oidc_rp_client_id = forms.CharField(
        label="Client ID",
        max_length=255,
        required=True,
        help_text="Your application's client ID from the OIDC provider",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    oidc_rp_client_secret = forms.CharField(
        label="Client Secret",
        max_length=255,
        required=True,
        help_text="Your application's client secret from the OIDC provider",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    # Provider Endpoints
    oidc_op_authorization_endpoint = forms.URLField(
        label="Authorization Endpoint",
        required=True,
        help_text="The OIDC provider's authorization endpoint URL",
        widget=forms.URLInput(attrs={"class": "form-control"}),
    )

    oidc_op_token_endpoint = forms.URLField(
        label="Token Endpoint",
        required=True,
        help_text="The OIDC provider's token endpoint URL",
        widget=forms.URLInput(attrs={"class": "form-control"}),
    )

    oidc_op_user_endpoint = forms.URLField(
        label="User Info Endpoint",
        required=True,
        help_text="The OIDC provider's user info endpoint URL",
        widget=forms.URLInput(attrs={"class": "form-control"}),
    )

    oidc_op_jwks_endpoint = forms.URLField(
        label="JWKS Endpoint",
        required=True,
        help_text="The OIDC provider's JWKS endpoint URL",
        widget=forms.URLInput(attrs={"class": "form-control"}),
    )

    # Optional Settings
    oidc_rp_sign_algo = forms.ChoiceField(
        label="Signing Algorithm",
        choices=[
            ("RS256", "RS256"),
            ("HS256", "HS256"),
            ("ES256", "ES256"),
        ],
        initial="RS256",
        required=False,
        help_text="Algorithm used to sign the ID token",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    oidc_rp_scopes = forms.CharField(
        label="Scopes",
        max_length=255,
        initial="openid email profile",
        required=False,
        help_text="Space-separated list of scopes to request",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    # Provider Type for pre-filling
    provider_type = forms.ChoiceField(
        label="Provider Type",
        choices=[
            ("", "Select Provider Type"),
            ("keycloak", "Keycloak"),
            ("google", "Google"),
            ("auth0", "Auth0"),
            ("custom", "Custom"),
        ],
        required=False,
        help_text="Select provider type to auto-fill endpoint URLs",
        widget=forms.Select(attrs={"class": "form-control", "onchange": "fillProviderEndpoints()"}),
    )

    provider_base_url = forms.URLField(
        label="Provider Base URL",
        required=False,
        help_text="Base URL for auto-filling endpoints",
        widget=forms.URLInput(attrs={"class": "form-control"}),
    )

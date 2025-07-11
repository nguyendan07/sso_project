import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.models import Session
from django.http import Http404, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from django.views.generic import View

from .forms import OIDCConfigForm


def healthz(request):
    """Health check endpoint."""
    return HttpResponse("OK")


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        """Get."""
        sessionid = request.COOKIES.get("sessionid")
        if not sessionid:
            raise Http404("Session not found")

        try:
            session = Session.objects.get(pk=sessionid)
            session_data = session.get_decoded()
        except Session.DoesNotExist:
            raise Http404("Session not found")

        csrf_token = get_token(request)
        csrf_token_html = ('<input type="hidden" name="csrfmiddlewaretoken" value="{}" />').format(
            csrf_token
        )

        return render(
            request,
            "home/index.html",
            {
                "settings": settings,
                "session_data": session_data,
                "csrf_token_html": csrf_token_html,
            },
            status=200,
        )


def is_superuser(user):
    """Check if user is superuser"""
    return user.is_superuser


@user_passes_test(is_superuser)
def oidc_config_view(request):
    """View for OIDC configuration form"""

    if request.method == "POST":
        form = OIDCConfigForm(request.POST)
        if form.is_valid():
            # Save configuration to environment or config file
            success = save_oidc_config(form.cleaned_data)
            if success:
                messages.success(
                    request,
                    "OIDC configuration saved successfully! Please restart the server to apply changes.",
                )
                return redirect("oidc_config")
            else:
                messages.error(
                    request, "Failed to save OIDC configuration. Please check file permissions."
                )
    else:
        # Pre-fill form with current settings
        initial_data = {
            "oidc_rp_client_id": getattr(settings, "OIDC_RP_CLIENT_ID", ""),
            "oidc_rp_client_secret": getattr(settings, "OIDC_RP_CLIENT_SECRET", ""),
            "oidc_op_authorization_endpoint": getattr(
                settings, "OIDC_OP_AUTHORIZATION_ENDPOINT", ""
            ),
            "oidc_op_token_endpoint": getattr(settings, "OIDC_OP_TOKEN_ENDPOINT", ""),
            "oidc_op_user_endpoint": getattr(settings, "OIDC_OP_USER_ENDPOINT", ""),
            "oidc_op_jwks_endpoint": getattr(settings, "OIDC_OP_JWKS_ENDPOINT", ""),
            "oidc_rp_sign_algo": getattr(settings, "OIDC_RP_SIGN_ALGO", "RS256"),
            "oidc_rp_scopes": getattr(settings, "OIDC_RP_SCOPES", "openid email profile"),
        }
        form = OIDCConfigForm(initial=initial_data)

    return render(request, "accounts/oidc_config.html", {"form": form})


def save_oidc_config(config_data):
    """Save OIDC configuration to .env file"""
    try:
        env_file_path = os.path.join(settings.BASE_DIR, ".env")

        # Read existing .env file
        existing_config = {}
        if os.path.exists(env_file_path):
            with open(env_file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        existing_config[key] = value

        # Update with new OIDC settings
        oidc_settings = {
            "OIDC_RP_CLIENT_ID": config_data["oidc_rp_client_id"],
            "OIDC_RP_CLIENT_SECRET": config_data["oidc_rp_client_secret"],
            "OIDC_OP_AUTHORIZATION_ENDPOINT": config_data["oidc_op_authorization_endpoint"],
            "OIDC_OP_TOKEN_ENDPOINT": config_data["oidc_op_token_endpoint"],
            "OIDC_OP_USER_ENDPOINT": config_data["oidc_op_user_endpoint"],
            "OIDC_OP_JWKS_ENDPOINT": config_data["oidc_op_jwks_endpoint"],
            "OIDC_RP_SIGN_ALGO": config_data["oidc_rp_sign_algo"],
            "OIDC_RP_SCOPES": config_data["oidc_rp_scopes"],
        }

        existing_config.update(oidc_settings)

        # Write updated configuration
        with open(env_file_path, "w") as f:
            for key, value in existing_config.items():
                f.write(f"{key}={value}\n")

        return True
    except Exception as e:
        print(f"Error saving OIDC config: {e}")
        return False

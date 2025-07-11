from django.conf import settings
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.models import Session
from django.middleware.csrf import get_token
from django.http import Http404


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

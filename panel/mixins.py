from django.shortcuts import redirect


class StaffRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('panel:login')
        return super().dispatch(request, *args, **kwargs)

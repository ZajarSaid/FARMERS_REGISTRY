from User.models import OutputVerification


def pending_verifications(request):
    if not request.user.is_authenticated:
        return {"pending_verifications": [], "pending_count": 0}

    verifications = OutputVerification.objects.filter(status="pending").order_by("-id")

    if not request.user.is_superuser:
        verifications = verifications.filter(owner=request.user)

    return {
        "pending_verifications": verifications,
        "pending_count": verifications.count(),
    }
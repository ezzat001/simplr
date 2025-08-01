def theme(request):
    theme = "light"
    if request.user.is_authenticated:
        theme = getattr(request.user.profile, "settings_theme", "light")
    return {"theme": theme}

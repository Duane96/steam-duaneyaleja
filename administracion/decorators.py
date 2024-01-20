from django.contrib.auth.decorators import user_passes_test

def admin_required(function=None, redirect_field_name=None, login_url='login'):
    """
    Decorador para vistas que verifica que el usuario loggeado es un administrador,
    redirige al login si es necesario.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,  # Cambia esta línea por la condición que quieras
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

from django.shortcuts import render
from .forms import AsistenteForm

def registro(request):
    if request.method == 'POST':
        form = AsistenteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'intensivo/registro_exitoso.html')
    else:
        form = AsistenteForm()
    return render(request, 'intensivo/registro.html', {'form': form})

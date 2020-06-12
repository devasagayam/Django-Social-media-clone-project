from django.shortcuts import render
from django.views.generic import CreateView
from profilewallet import models,forms
from django.urls import reverse_lazy
# Create your views here.
class CreateWallet(CreateView):
    template_name='wallet_form.html'
    form_class=forms.WalletForm
    model=models.Wallet
    success_url=reverse_lazy("home")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

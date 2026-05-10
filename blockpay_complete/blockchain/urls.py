from django.urls import path
from . import views

urlpatterns = [
    path("",                          views.index,                    name="index"),
    path("api/chain/",                views.ChainView.as_view(),      name="chain"),
    path("api/wallets/",              views.WalletsView.as_view(),    name="wallets"),
    path("api/balance/<str:address>/",views.BalanceView.as_view(),    name="balance"),
    path("api/transactions/",         views.TransactionView.as_view(),name="transactions"),
    path("api/mine/",                 views.MineView.as_view(),       name="mine"),
    path("api/validate/",             views.ValidateView.as_view(),   name="validate"),
]

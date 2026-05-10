from django.contrib import admin
from .models import Currency, ExpenseCategory, PaymentMethod, Expense

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currency_name', 'currency_symbol')
    search_fields = ('currency_name', 'currency_symbol')

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'user', 'item_cost', 'currency', 'status', 'created_at')
    list_filter = ('status', 'currency', 'expense_category', 'payment_method')
    search_fields = ('item_name', 'description')
    readonly_fields = ('created_at', 'updated_at')

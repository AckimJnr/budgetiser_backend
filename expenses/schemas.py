from ninja import ModelSchema
from .models import Currency, ExpenseCategory, PaymentMethod, Expense

class CurrencySchema(ModelSchema):
    class Config:
        model = Currency
        model_fields = ['id', 'currency_name', 'currency_symbol']

class ExpenseCategorySchema(ModelSchema):
    class Config:
        model = ExpenseCategory
        model_fields = ['id', 'name', 'description']

class PaymentMethodSchema(ModelSchema):
    class Config:
        model = PaymentMethod
        model_fields = ['id', 'name']

class ExpenseSchema(ModelSchema):
    class Config:
        model = Expense
        model_fields = [
            'id', 'user', 'item_name', 'item_cost', 'currency', 'quantity', 
            'status', 'description', 'expense_category', 'payment_method', 
            'created_at', 'updated_at'
        ]

class ExpenseCreateSchema(ModelSchema):
    class Config:
        model = Expense
        model_fields = [
            'user', 'item_name', 'item_cost', 'currency', 'quantity', 
            'status', 'description', 'expense_category', 'payment_method'
        ]

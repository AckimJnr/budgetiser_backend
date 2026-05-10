from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from .models import Currency, ExpenseCategory, PaymentMethod, Expense
from .schemas import (
    CurrencySchema, ExpenseCategorySchema, PaymentMethodSchema,
    ExpenseSchema, ExpenseCreateSchema
)

router = Router(tags=["Expenses"])

# Currencies
@router.get("/currencies/", response=List[CurrencySchema])
def list_currencies(request):
    return Currency.objects.all()

# Categories
@router.get("/categories/", response=List[ExpenseCategorySchema])
def list_categories(request):
    return ExpenseCategory.objects.all()

# Payment Methods
@router.get("/payment-methods/", response=List[PaymentMethodSchema])
def list_payment_methods(request):
    return PaymentMethod.objects.all()

# Expenses
@router.post("/", response={201: ExpenseSchema})
def create_expense(request, data: ExpenseCreateSchema):
    expense = Expense.objects.create(**data.dict())
    return 201, expense

@router.get("/", response=List[ExpenseSchema])
def list_expenses(request):
    return Expense.objects.all()

@router.get("/{expense_id}", response=ExpenseSchema)
def get_expense(request, expense_id: int):
    expense = get_object_or_404(Expense, id=expense_id)
    return expense

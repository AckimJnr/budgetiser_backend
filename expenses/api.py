from datetime import date
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from accounts.security import JWTAuth
from .models import Currency, ExpenseCategory, PaymentMethod, Expense
from .schemas import (
    AuthExpenseCreateSchema,
    AuthExpenseUpdateSchema,
    CurrencySchema,
    ExpenseCategorySchema,
    ExpenseSchema,
    PaymentMethodSchema,
)

router = Router(tags=["Expenses"], auth=JWTAuth())


def _parse_date(value: str | None) -> date:
    if not value:
        return date.today()
    parts = value.strip()[:10].split("-")
    if len(parts) != 3:
        return date.today()
    y, m, d = (int(parts[0]), int(parts[1]), int(parts[2]))
    return date(y, m, d)


@router.get("/currencies/", response=List[CurrencySchema])
def list_currencies(request):
    return Currency.objects.all()


@router.get("/categories/", response=List[ExpenseCategorySchema])
def list_categories(request):
    return ExpenseCategory.objects.all()


@router.get("/payment-methods/", response=List[PaymentMethodSchema])
def list_payment_methods(request):
    return PaymentMethod.objects.all()


@router.post("/", response={201: ExpenseSchema})
def create_expense(request, data: AuthExpenseCreateSchema):
    user = request.auth
    expense = Expense.objects.create(
        user=user,
        expense_date=_parse_date(data.expense_date),
        item_name=data.item_name,
        item_cost=data.item_cost,
        currency_id=data.currency,
        quantity=data.quantity,
        status=data.status,
        description=data.description,
        expense_category_id=data.expense_category,
        payment_method_id=data.payment_method,
    )
    return 201, expense


@router.get("/", response=List[ExpenseSchema])
def list_expenses(request):
    return Expense.objects.filter(user=request.auth).order_by("-expense_date", "-id")


@router.get("/{expense_id}", response=ExpenseSchema)
def get_expense(request, expense_id: int):
    return get_object_or_404(Expense, id=expense_id, user=request.auth)


@router.put("/{expense_id}", response=ExpenseSchema)
def update_expense(request, expense_id: int, data: AuthExpenseUpdateSchema):
    expense = get_object_or_404(Expense, id=expense_id, user=request.auth)
    payload = data.dict(exclude_unset=True)
    if "expense_date" in payload:
        expense.expense_date = _parse_date(payload.pop("expense_date"))
    if "currency" in payload:
        expense.currency_id = payload.pop("currency")
    if "expense_category" in payload:
        expense.expense_category_id = payload.pop("expense_category")
    if "payment_method" in payload:
        expense.payment_method_id = payload.pop("payment_method")
    for key, value in payload.items():
        setattr(expense, key, value)
    expense.save()
    return expense


@router.delete("/{expense_id}", response={204: None})
def delete_expense(request, expense_id: int):
    expense = get_object_or_404(Expense, id=expense_id, user=request.auth)
    expense.delete()
    return 204, None

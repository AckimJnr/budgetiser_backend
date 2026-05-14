from decimal import Decimal
from typing import Optional

from ninja import ModelSchema, Schema
from pydantic import Field

from .models import Currency, ExpenseCategory, PaymentMethod, Expense


class CurrencySchema(ModelSchema):
    class Config:
        model = Currency
        model_fields = ["id", "currency_name", "currency_symbol"]


class ExpenseCategorySchema(ModelSchema):
    class Config:
        model = ExpenseCategory
        model_fields = ["id", "name", "description"]


class PaymentMethodSchema(ModelSchema):
    class Config:
        model = PaymentMethod
        model_fields = ["id", "name"]


class ExpenseSchema(ModelSchema):
    class Config:
        model = Expense
        model_fields = [
            "id",
            "user",
            "expense_date",
            "item_name",
            "item_cost",
            "currency",
            "quantity",
            "status",
            "description",
            "expense_category",
            "payment_method",
            "created_at",
            "updated_at",
        ]


class ExpenseCreateSchema(ModelSchema):
    class Config:
        model = Expense
        model_fields = [
            "user",
            "expense_date",
            "item_name",
            "item_cost",
            "currency",
            "quantity",
            "status",
            "description",
            "expense_category",
            "payment_method",
        ]


class AuthExpenseCreateSchema(Schema):
    expense_date: Optional[str] = None
    item_name: str = Field(..., min_length=1, max_length=255)
    item_cost: Decimal = Field(..., gt=0)
    currency: int
    quantity: int = Field(default=1, ge=1)
    status: str = Field(default="pending")
    description: Optional[str] = None
    expense_category: Optional[int] = None
    payment_method: Optional[int] = None


class AuthExpenseUpdateSchema(Schema):
    expense_date: Optional[str] = None
    item_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    item_cost: Optional[Decimal] = Field(default=None, gt=0)
    currency: Optional[int] = None
    quantity: Optional[int] = Field(default=None, ge=1)
    status: Optional[str] = None
    description: Optional[str] = None
    expense_category: Optional[int] = None
    payment_method: Optional[int] = None

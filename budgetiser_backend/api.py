from ninja import NinjaAPI
from accounts.api import router as accounts_router
from expenses.api import router as expenses_router

api_v1 = NinjaAPI(title="Budgetiser API", version="1.0.0", urls_namespace="v1")

api_v1.add_router("/accounts/", accounts_router)
api_v1.add_router("/expenses/", expenses_router)

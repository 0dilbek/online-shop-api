from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.core.config import settings
from app.db.session import engine
from app.admin.views import (
    AdminUserAdmin,
    CategoryAdmin,
    ProductAdmin,
    OrderAdmin,
    OrderItemAdmin,
    CustomerAdmin,
)
from app.admin.auth import AdminAuth
from app.api.v1 import categories, products, orders, cart, customer
from app.admin import orders_dashboard


tags_metadata = [
    {
        "name": "categories",
        "description": "Mahsulot kategoriyalarini olish uchun endpointlar.",
    },
    {
        "name": "products",
        "description": "Mahsulotlar ro'yxati, filter, qidirish va boshqalar.",
    },
    {
        "name": "cart",
        "description": "Savat (cart) bilan ishlash: qo'shish, o'chirish, yangilash.",
    },
    {
        "name": "orders",
        "description": "Buyurtma yaratish va buyurtma holatini ko'rish.",
    },
]

app = FastAPI(
    title="Online Shop API",
    description="Android ilova uchun online do'kon backend API. Savat, buyurtma va mahsulotlar bilan ishlash uchun.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# statik fayllar
app.mount("/static", StaticFiles(directory="static"), name="static")

# session + admin auth
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(AdminUserAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(ProductAdmin)
admin.add_view(OrderAdmin)
admin.add_view(OrderItemAdmin)
admin.add_view(CustomerAdmin)

# API routerlar
app.include_router(categories.router, prefix="/api/v1", tags=["categories"])
app.include_router(products.router,  prefix="/api/v1", tags=["products"])
app.include_router(cart.router,      prefix="/api/v1", tags=["cart"])
app.include_router(orders.router,    prefix="/api/v1", tags=["orders"])
app.include_router(customer.router,  prefix="/api/v1", tags=["customers"])
app.include_router(orders_dashboard.router, tags=["admin-custom"])


@app.get("/")
def read_root():
    return {"message": "Online shop API is running"}

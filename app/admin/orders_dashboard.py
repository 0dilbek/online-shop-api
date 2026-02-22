from fastapi import APIRouter, Request, Depends, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from app.api.deps import get_db
from app.models.order import Order
import math

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/admin/custom/orders")
def get_orders_dashboard(
    request: Request,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    offset = (page - 1) * limit
    
    # Eager load items and products to avoid N+1 issues
    orders_query = db.query(Order).options(
        joinedload(Order.items)
    ).order_by(Order.created_at.desc())
    
    total_count = orders_query.count()
    orders = orders_query.offset(offset).limit(limit).all()
    
    total_pages = math.ceil(total_count / limit)
    
    return templates.TemplateResponse(
        "admin/orders.html",
        {
            "request": request,
            "orders": orders,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "total_count": total_count,
        }
    )

from fastapi import APIRouter, Request, Depends, Query, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from app.api.deps import get_db
from app.models.order import Order
from pydantic import BaseModel
import math

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

class StatusUpdate(BaseModel):
    status: str

@router.get("/dashboard/orders")
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
            "statuses": ["new", "confirmed", "delivering", "completed", "canceled"]
        }
    )

@router.post("/dashboard/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    payload: StatusUpdate,
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    valid_statuses = ["new", "confirmed", "delivering", "completed", "canceled"]
    if payload.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    order.status = payload.status
    db.commit()
    db.refresh(order)
    
    return {"status": "success", "new_status": order.status}

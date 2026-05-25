from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.inventory_model import BloodInventory
from app.schemas.inventory_schema import InventoryCreate, InventoryUpdate

router = APIRouter()

# Helper function to build inventory response
def build_inventory_payload(item: BloodInventory):
    return {
        "id": item.id,
        "blood_group": item.blood_group,
        "units": item.units,
        "status": "CRITICAL" if item.units < 5 else "LOW" if item.units < 10 else "HEALTHY"
    }

# CREATE INVENTORY
@router.post("/inventory")
@router.post("/admin/inventory")
def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    existing = db.query(BloodInventory).filter(
        BloodInventory.blood_group == inventory.blood_group
    ).first()
    if existing:
        existing.units += inventory.units
        db.commit()
        db.refresh(existing)
        return {
            "message": "Inventory updated successfully",
            "inventory": build_inventory_payload(existing)
        }

    new_inventory = BloodInventory(
        blood_group=inventory.blood_group,
        units=inventory.units
    )
    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)
    return {
        "message": "Inventory added successfully",
        "inventory": build_inventory_payload(new_inventory)
    }

# GET INVENTORY
@router.get("/inventory")
@router.get("/admin/inventory")
def get_inventory(db: Session = Depends(get_db)):
    inventory = db.query(BloodInventory).all()
    return [build_inventory_payload(item) for item in inventory]

# UPDATE INVENTORY
@router.put("/inventory/{inventory_id}")
@router.put("/admin/inventory/{inventory_id}")
def update_inventory(
    inventory_id: int,
    inventory: InventoryUpdate,
    db: Session = Depends(get_db)
):
    existing = db.query(BloodInventory).filter(
        BloodInventory.id == inventory_id
    ).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Inventory not found")

    if inventory.blood_group is not None:
        existing.blood_group = inventory.blood_group
    if inventory.units is not None:
        existing.units = inventory.units

    db.commit()
    db.refresh(existing)
    return {
        "message": "Inventory updated successfully",
        "inventory": build_inventory_payload(existing)
    }

# DELETE INVENTORY
@router.delete("/inventory/{inventory_id}")
@router.delete("/admin/inventory/{inventory_id}")
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    existing = db.query(BloodInventory).filter(
        BloodInventory.id == inventory_id
    ).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Inventory not found")

    db.delete(existing)
    db.commit()
    return {"message": "Inventory deleted successfully"}

# LOW STOCK ALERT
@router.get("/inventory/low-stock")
@router.get("/admin/inventory/low-stock")
def low_stock_alert(db: Session = Depends(get_db)):
    low_stock = db.query(BloodInventory).filter(
        BloodInventory.units < 5
    ).all()
    return {"low_stock_inventory": [build_inventory_payload(item) for item in low_stock]}

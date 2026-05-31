from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from config.database import get_session
from model.models import BubbleTea
from model.schemas import BubbleTeaCreate, BubbleTeaRead, BubbleTeaUpdate

router = APIRouter(prefix="/bubbleteas", tags=["bubbleteas"])


def _serialize(item: BubbleTea) -> dict:
    return BubbleTeaRead.model_validate(item, from_attributes=True).model_dump()


def _not_found():
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"ok": False, "results": "BubbleTea not found"},
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_bubbletea(
    payload: BubbleTeaCreate,
    session: Session = Depends(get_session),
):
    item = BubbleTea(**payload.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return {"ok": True, "results": _serialize(item)}


@router.get("/")
def list_bubbleteas(
    session: Session = Depends(get_session),
):
    items = session.scalars(select(BubbleTea).where(BubbleTea.active.is_(True))).all()
    return {"ok": True, "results": [_serialize(i) for i in items]}


@router.get("/{bubbletea_id}")
def get_bubbletea(
    bubbletea_id: int,
    session: Session = Depends(get_session),
):
    item = session.scalar(
        select(BubbleTea).where(BubbleTea.id == bubbletea_id, BubbleTea.active.is_(True))
    )
    if item is None:
        return _not_found()
    return {"ok": True, "results": _serialize(item)}


@router.put("/{bubbletea_id}")
def update_bubbletea(
    bubbletea_id: int,
    payload: BubbleTeaUpdate,
    session: Session = Depends(get_session),
):
    item = session.get(BubbleTea, bubbletea_id)
    if item is None:
        return _not_found()

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    session.commit()
    session.refresh(item)
    return {"ok": True, "results": _serialize(item)}


@router.delete("/{bubbletea_id}")
def delete_bubbletea(
    bubbletea_id: int,
    session: Session = Depends(get_session),
):
    item = session.get(BubbleTea, bubbletea_id)
    if item is None:
        return _not_found()
    session.delete(item)
    session.commit()
    return {"ok": True, "results": None}

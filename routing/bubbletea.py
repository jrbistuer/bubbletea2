from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from config.database import get_session
from model.models import BubbleTea
from model.schemas import BubbleTeaCreate, BubbleTeaRead, BubbleTeaUpdate

router = APIRouter(prefix="/bubbleteas", tags=["bubbleteas"])


@router.post("/", response_model=BubbleTeaRead, status_code=status.HTTP_201_CREATED)
def create_bubbletea(
    payload: BubbleTeaCreate,
    session: Session = Depends(get_session),
) -> BubbleTea:
    item = BubbleTea(**payload.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("/", response_model=list[BubbleTeaRead])
def list_bubbleteas(
    session: Session = Depends(get_session),
) -> list[BubbleTea]:
    return list(session.scalars(select(BubbleTea)).all())


@router.get("/{bubbletea_id}", response_model=BubbleTeaRead)
def get_bubbletea(
    bubbletea_id: int,
    session: Session = Depends(get_session),
) -> BubbleTea:
    item = session.get(BubbleTea, bubbletea_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BubbleTea not found")
    return item


@router.put("/{bubbletea_id}", response_model=BubbleTeaRead)
def update_bubbletea(
    bubbletea_id: int,
    payload: BubbleTeaUpdate,
    session: Session = Depends(get_session),
) -> BubbleTea:
    item = session.get(BubbleTea, bubbletea_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BubbleTea not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    session.commit()
    session.refresh(item)
    return item


@router.delete("/{bubbletea_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bubbletea(
    bubbletea_id: int,
    session: Session = Depends(get_session),
) -> None:
    item = session.get(BubbleTea, bubbletea_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BubbleTea not found")
    session.delete(item)
    session.commit()

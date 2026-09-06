from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.repositories.mission_repo import (
    create_mission,
    get_missions,
    get_mission_by_id,
    delete_mission,
    update_mission_status,
)
from app.schemas.mission import MissionCreate, MissionStatusUpdate


def write_mission_log(message: str):
    with open("mission_events.log", "a") as file:
        file.write(message + "\n")


router = APIRouter()


@router.post("/missions")
def create_mission_route(
    mission: MissionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    created_mission = create_mission(db, mission)

    background_tasks.add_task(
        write_mission_log, 
        f"Mission created: {created_mission.id}"
    )
    return created_mission


@router.get("/missions")
def get_missions_route(
    db: Session = Depends(get_db),
):
    return get_missions(db)


@router.get("/missions/{mission_id}")
def get_mission_route(
    mission_id: int,
    db: Session = Depends(get_db),
):
    mission = get_mission_by_id(db, mission_id)

    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    return mission


@router.delete("/missions/{mission_id}")
def delete_mission_route(
    mission_id: int,
    db: Session = Depends(get_db),
):
    mission = get_mission_by_id(db, mission_id)

    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    delete_mission(db, mission)

    return {"message": "Mission deleted"}


@router.patch("/missions/{mission_id}/status")
def update_mission_status_route(
    mission_id: int,
    data: MissionStatusUpdate,
    db: Session = Depends(get_db),
):
    mission = get_mission_by_id(db, mission_id)

    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    return update_mission_status(db, mission, data.status)

from sqlalchemy.orm import Session

from app.models.mission import Mission
from app.schemas.mission import MissionCreate


def create_mission(db: Session, mission: MissionCreate):
    db_mission = Mission(
        name=mission.name,
        object_name=mission.object_name,
        status=mission.status,
        planned_date=mission.planned_date,
        notes=mission.notes,
    )

    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)

    return db_mission


def get_missions(db: Session):
    return db.query(Mission).all()


def get_mission_by_id(db: Session, mission_id: int):
    return db.query(Mission).filter(Mission.id == mission_id).first()


def delete_mission(db: Session, mission: Mission):
    db.delete(mission)
    db.commit()


def update_mission_status(
    db: Session,
    mission: Mission,
    status: str,
):
    mission.status = status
    db.commit()
    db.refresh(mission)

    return mission

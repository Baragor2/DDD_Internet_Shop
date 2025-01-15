from infra.models.base import BaseModel


def model_to_document(model: BaseModel):
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}

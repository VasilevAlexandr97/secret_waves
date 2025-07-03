import uuid


class EntityNotFoundError(Exception):
    def __init__(self, entity_name: str, entity_id: int | uuid.UUID):
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} with id {entity_id} not found")

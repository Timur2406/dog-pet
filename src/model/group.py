from pydantic import BaseModel


# === Breed Reference Model ===
class BreedReference(BaseModel):
    id: str | None = None
    type: str | None = None


# === Breeds Relationship Model ===
class BreedsRelationshipData(BaseModel):
    data: list[BreedReference] | None = None


# === Relationships Model ===
class GroupRelationships(BaseModel):
    breeds: BreedsRelationshipData | None = None


# === Attributes Model ===
class GroupAttributes(BaseModel):
    name: str | None = None


# === Main Group Data Model ===
class GroupDataItem(BaseModel):
    id: str | None = None
    type: str | None = None
    attributes: GroupAttributes | None = None
    relationships: GroupRelationships | None = None


# === Links Model ===
class LinksData(BaseModel):
    self: str | None = None
    current: str | None = None
    first: str | None = None
    prev: str | None = None


# === Root Model ===
class DogGroupResponse(BaseModel):
    data: list[GroupDataItem] | None = None
    links: LinksData | None = None


class DogCurrentGroupResponse(BaseModel):
    data: GroupDataItem | None = None
    links: LinksData | None = None

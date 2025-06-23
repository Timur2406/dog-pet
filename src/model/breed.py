from pydantic import BaseModel


# === Weight and Life Models ===
class WeightInfo(BaseModel):
    max: int | None = None
    min: int | None = None


class RelationshipsData(BaseModel):
    id: str | None = None
    type: str | None = None


# === Relationships Models ===
class GroupData(BaseModel):
    data: RelationshipsData | None = None


class GroupRelationships(BaseModel):
    group: GroupData | None = None


# === Attributes Model ===
class BreedAttributes(BaseModel):
    name: str | None = None
    description: str | None = None
    life: WeightInfo | None = None
    male_weight: WeightInfo | None = None
    female_weight: WeightInfo | None = None
    hypoallergenic: bool | None = None


# === Main Breed Data Model ===
class BreedDataItem(BaseModel):
    id: str | None = None
    type: str | None = None
    attributes: BreedAttributes | None = None
    relationships: GroupRelationships | None = None


# === Pagination Meta Model ===
class PaginationMeta(BaseModel):
    current: int | None = None
    next: int | None = None
    last: int | None = None
    records: int


class MetaData(BaseModel):
    pagination: PaginationMeta


# === Links Model ===
class LinksData(BaseModel):
    self: str | None = None
    current: str | None = None
    next: str | None = None
    last: str | None = None
    prev: str | None = None


# === Root Model ===
class DogBreedResponse(BaseModel):
    data: list[BreedDataItem] | None = None
    meta: MetaData
    links: LinksData | None = None


class DogCurrentBreedResponse(BaseModel):
    data: BreedDataItem | None = None
    links: LinksData | None = None

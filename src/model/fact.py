from pydantic import BaseModel


# === Attributes Model ===
class FactAttributes(BaseModel):
    body: str | None = None


# === Data Item Model ===
class FactDataItem(BaseModel):
    id: str | None = None
    type: str | None = None
    attributes: FactAttributes | None = None


# === Root Model ===
class DogFactResponse(BaseModel):
    data: list[FactDataItem] | None = None

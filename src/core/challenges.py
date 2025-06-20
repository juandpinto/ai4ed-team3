from abc import abstractmethod
from typing import ClassVar, Dict, Type, Any, List, Self, Tuple
from pydantic import BaseModel, Field


class BaseChallenge(BaseModel):
    challenge_type: str = Field(..., description="The type of the challenge")

    _registry: ClassVar[Dict[str, Type["BaseChallenge"]]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "type_key"):
            BaseChallenge._registry[cls.type_key] = cls

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseChallenge":
        type_key = data.get("challenge_type")
        if type_key not in cls._registry:
            raise ValueError(f"Unknown challenge type: {type_key}")
        return cls._registry[type_key](**data)

    def to_dict(self) -> dict:
        return self.model_dump()

    @classmethod
    def get_class_by_type(cls, type_key: str) -> type["BaseChallenge"]:
        return cls._registry[type_key]

    @classmethod
    def get_example_for(cls, type_key: str) -> dict:
        if type_key not in cls._registry:
            raise ValueError(f"Unknown challenge type: {type_key}")
        return cls._registry[type_key].example().model_dump()

    @classmethod
    @abstractmethod
    def example(cls) -> "BaseChallenge":
        """Return a dummy example instance"""
        raise NotImplementedError

    def summarize(self) -> "BaseChallenge":
        """Use this method to resolve a base challenge to its specific type"""
        raise NotImplementedError


class Pairing(BaseModel):
    words: Tuple[str, str] = Field(description="Tuple of words that are associated")
    justification: str = Field(default="String representing the justification for the pairing")


class ChallengeTriplet(BaseChallenge):
    type_key: str = "triplet"
    challenge_type: str = "triplet"

    triplet: Tuple[str, str, str] = Field(description="Word triplets for association")
    pairings: List[Pairing] = Field(description="List of pairings with their associated definitions")

    def summarize(self) -> Self:
        return self

    @classmethod
    def class_type(cls) -> type["BaseChallenge"]:
        return cls

    @classmethod
    def example(cls) -> "ChallengeTriplet":
        return cls(
            triplet=("dog", "cat", "bone"),
            pairings=[
                {"words": ("dog", "cat"), "justification": "because they are both animals"},
                {"words": ("dog", "bone"), "justification": "because dogs like bones"}
            ]
        )

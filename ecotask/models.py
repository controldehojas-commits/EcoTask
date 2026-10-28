from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


class ImpactLevel:
    """Impact weights used to estimate the simulated carbon footprint."""

    MAPPING = {
        "low": 1,
        "medium": 3,
        "high": 5,
    }

    @classmethod
    def values(cls) -> list[str]:
        return list(cls.MAPPING.keys())


@dataclass
class Task:
    """Represents one sustainable task entry."""

    title: str
    description: str = ""
    completed: bool = False
    impact: str = "low"
    category: str = "general"
    id: str = field(default_factory=lambda: str(uuid4()))

    @property
    def impact_weight(self) -> int:
        return ImpactLevel.MAPPING.get(self.impact.lower(), 1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "impact": self.impact.lower(),
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        return cls(
            id=data.get("id") or str(uuid4()),
            title=data.get("title", ""),
            description=data.get("description", ""),
            completed=bool(data.get("completed", False)),
            impact=str(data.get("impact", "low")).lower(),
            category=data.get("category", "general"),
        )

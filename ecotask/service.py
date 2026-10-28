from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .models import ImpactLevel, Task
from .storage import JsonStorage


class TaskManager:
    """Business logic for creating, reading, updating, and deleting tasks."""

    def __init__(self, storage_path: str | Path | None = None):
        self.storage = JsonStorage(storage_path or Path("data") / "tasks.json")

    def _load_tasks(self) -> list[Task]:
        return [Task.from_dict(item) for item in self.storage.load()]

    def _save_tasks(self, tasks: Iterable[Task]) -> None:
        self.storage.save([task.to_dict() for task in tasks])

    def create_task(self, title: str, description: str = "", impact: str = "low", category: str = "general") -> Task:
        normalized_title = title.strip()
        if not normalized_title:
            raise ValueError("The title cannot be empty.")

        impact_key = str(impact).lower()
        if impact_key not in ImpactLevel.values():
            raise ValueError(f"Impact must be one of: {', '.join(ImpactLevel.values())}.")

        task = Task(title=normalized_title, description=description.strip(), impact=impact_key, category=category.strip() or "general")
        tasks = self._load_tasks()
        tasks.append(task)
        self._save_tasks(tasks)
        return task

    def list_tasks(self) -> list[Task]:
        return self._load_tasks()

    def get_task(self, task_id: str) -> Task | None:
        for task in self._load_tasks():
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: str, **updates) -> Task | None:
        tasks = self._load_tasks()
        for index, task in enumerate(tasks):
            if task.id == task_id:
                for key, value in updates.items():
                    if key == "title":
                        if not str(value).strip():
                            raise ValueError("The title cannot be empty.")
                        task.title = str(value).strip()
                    elif key == "description":
                        task.description = str(value).strip()
                    elif key == "completed":
                        task.completed = bool(value)
                    elif key == "impact":
                        normalized = str(value).lower()
                        if normalized not in ImpactLevel.values():
                            raise ValueError(f"Impact must be one of: {', '.join(ImpactLevel.values())}.")
                        task.impact = normalized
                    elif key == "category":
                        task.category = str(value).strip() or "general"
                self._save_tasks(tasks)
                return task
        return None

    def delete_task(self, task_id: str) -> bool:
        tasks = self._load_tasks()
        remaining = [task for task in tasks if task.id != task_id]
        if len(remaining) == len(tasks):
            return False
        self._save_tasks(remaining)
        return True

    def total_carbon_footprint(self, tasks: list[Task] | None = None) -> int:
        selected = tasks if tasks is not None else self._load_tasks()
        return sum(task.impact_weight for task in selected)

    def generate_report(self, tasks: list[Task] | None = None) -> dict[str, int | str]:
        selected = tasks if tasks is not None else self._load_tasks()
        stats = {
            "total_tasks": len(selected),
            "completed": sum(1 for task in selected if task.completed),
            "pending": sum(1 for task in selected if not task.completed),
            "low_impact": sum(1 for task in selected if task.impact == "low"),
            "medium_impact": sum(1 for task in selected if task.impact == "medium"),
            "high_impact": sum(1 for task in selected if task.impact == "high"),
            "carbon_footprint": self.total_carbon_footprint(selected),
        }
        if stats["carbon_footprint"] <= 5:
            stats["carbon_level"] = "low"
        elif stats["carbon_footprint"] <= 15:
            stats["carbon_level"] = "moderate"
        else:
            stats["carbon_level"] = "high"
        return stats

    def eco_suggestions(self, tasks: list[Task] | None = None) -> list[str]:
        selected = tasks if tasks is not None else self._load_tasks()
        suggestions = [
            "Use public transportation for your next task outside the home.",
            "Recycle materials or paper whenever possible during task execution.",
            "Prefer a single local errand instead of several short trips.",
        ]
        if any(task.category.lower() == "home" for task in selected):
            suggestions.append("Plan a home task session to reduce unnecessary energy use.")
        if any(task.impact == "high" for task in selected):
            suggestions.append("Review high-impact tasks and combine them with lower-impact activities.")
        return suggestions[:4]

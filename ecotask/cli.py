from __future__ import annotations

from pathlib import Path

from .service import TaskManager


LANGUAGE_PACKS = {
    "es": {
        "title": "EcoTask - Gestor de Tareas Sostenible",
        "choose_language": "Selecciona idioma / Choose language (es/en): ",
        "menu": "\n1. Crear tarea\n2. Ver tareas\n3. Actualizar tarea\n4. Eliminar tarea\n5. Informe ambiental\n6. Cambiar idioma\n0. Salir\n",
        "enter_title": "Título: ",
        "enter_description": "Descripción: ",
        "enter_impact": "Impacto estimado (low/medium/high): ",
        "enter_category": "Categoría: ",
        "task_created": "Tarea creada correctamente.",
        "task_deleted": "Tarea eliminada.",
        "task_not_found": "No se encontró la tarea.",
        "task_updated": "Tarea actualizada.",
        "task_id": "ID de la tarea: ",
        "view_tasks": "Tareas registradas:",
        "report": "Reporte de huella de carbono simulada:",
        "suggestions": "Sugerencias sostenibles:",
        "language_changed": "Idioma cambiado.",
        "invalid_choice": "Opción no válida.",
        "goodbye": "¡Gracias por usar EcoTask!",
        "none": "No hay tareas registradas.",
    },
    "en": {
        "title": "EcoTask - Sustainable Task Manager",
        "choose_language": "Select language / Elige idioma (es/en): ",
        "menu": "\n1. Create task\n2. View tasks\n3. Update task\n4. Delete task\n5. Environmental report\n6. Change language\n0. Exit\n",
        "enter_title": "Title: ",
        "enter_description": "Description: ",
        "enter_impact": "Estimated impact (low/medium/high): ",
        "enter_category": "Category: ",
        "task_created": "Task created successfully.",
        "task_deleted": "Task deleted.",
        "task_not_found": "Task not found.",
        "task_updated": "Task updated.",
        "task_id": "Task ID: ",
        "view_tasks": "Registered tasks:",
        "report": "Simulated carbon footprint report:",
        "suggestions": "Sustainable suggestions:",
        "language_changed": "Language changed.",
        "invalid_choice": "Invalid option.",
        "goodbye": "Thanks for using EcoTask!",
        "none": "No tasks registered.",
    },
}


class TaskCLI:
    """Simple interactive console interface."""

    def __init__(self, storage_path: str | Path | None = None, language: str = "es"):
        self.manager = TaskManager(storage_path)
        self.language = language.lower() if language.lower() in LANGUAGE_PACKS else "es"

    def text(self, key: str) -> str:
        return LANGUAGE_PACKS[self.language][key]

    def prompt_language(self) -> None:
        try:
            raw = input(self.text("choose_language")).strip().lower()
        except (EOFError, KeyboardInterrupt):
            return
        if raw in LANGUAGE_PACKS:
            self.language = raw

    def create_task(self) -> None:
        try:
            title = input(self.text("enter_title")).strip()
        except (EOFError, KeyboardInterrupt):
            return
        if not title:
            print(self.text("invalid_choice"))
            return
        try:
            description = input(self.text("enter_description")).strip()
            impact = input(self.text("enter_impact")).strip().lower() or "low"
            category = input(self.text("enter_category")).strip() or "general"
        except (EOFError, KeyboardInterrupt):
            return
        try:
            task = self.manager.create_task(title, description, impact, category)
            print(f"{self.text('task_created')} ID: {task.id}")
        except ValueError as exc:
            print(str(exc))

    def view_tasks(self) -> None:
        tasks = self.manager.list_tasks()
        if not tasks:
            print(self.text("none"))
            return
        print(self.text("view_tasks"))
        for task in tasks:
            status = "Done" if task.completed else "Pending"
            status = status if self.language == "en" else ("Hecha" if task.completed else "Pendiente")
            print(f"- {task.title} [{task.impact}] ({status}) | {task.category} | {task.id}")
            if task.description:
                print(f"  {task.description}")

    def update_task(self) -> None:
        try:
            task_id = input(self.text("task_id")).strip()
        except (EOFError, KeyboardInterrupt):
            return
        task = self.manager.get_task(task_id)
        if task is None:
            print(self.text("task_not_found"))
            return

        try:
            new_title = input(f"{self.text('enter_title')} [{task.title}]: ").strip() or task.title
            new_description = input(f"{self.text('enter_description')} [{task.description or '-'}]: ").strip() or task.description
            new_impact = input(f"{self.text('enter_impact')} [{task.impact}]: ").strip().lower() or task.impact
            new_category = input(f"{self.text('enter_category')} [{task.category}]: ").strip() or task.category
            completed = input("Completed? (y/N): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return
        try:
            updated = self.manager.update_task(
                task_id,
                title=new_title,
                description=new_description,
                impact=new_impact,
                category=new_category,
                completed=(completed in {"y", "yes", "true", "1"}),
            )
            if updated is not None:
                print(self.text("task_updated"))
        except ValueError as exc:
            print(str(exc))

    def delete_task(self) -> None:
        try:
            task_id = input(self.text("task_id")).strip()
        except (EOFError, KeyboardInterrupt):
            return
        if self.manager.delete_task(task_id):
            print(self.text("task_deleted"))
        else:
            print(self.text("task_not_found"))

    def show_report(self) -> None:
        tasks = self.manager.list_tasks()
        report = self.manager.generate_report(tasks)
        print(self.text("report"))
        print(f"Total tasks: {report['total_tasks']}")
        print(f"Completed: {report['completed']} | Pending: {report['pending']}")
        print(f"Carbon footprint: {report['carbon_footprint']} points | Level: {report['carbon_level']}")
        print(f"Low: {report['low_impact']} | Medium: {report['medium_impact']} | High: {report['high_impact']}")
        print(self.text("suggestions"))
        for suggestion in self.manager.eco_suggestions(tasks):
            print(f"- {suggestion}")

    def run(self) -> None:
        self.prompt_language()
        print(self.text("title"))
        while True:
            try:
                print(self.text("menu"), end="")
                choice = input("Option: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n" + self.text("goodbye"))
                break
            if choice == "1":
                self.create_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.show_report()
            elif choice == "6":
                self.prompt_language()
                print(self.text("language_changed"))
            elif choice == "0":
                print(self.text("goodbye"))
                break
            else:
                print(self.text("invalid_choice"))


def main() -> None:
    TaskCLI(storage_path=Path("data") / "tasks.json").run()


if __name__ == "__main__":
    main()

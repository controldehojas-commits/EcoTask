import tempfile
import unittest
from pathlib import Path

from ecotask.service import TaskManager


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.temp_dir.name) / "tasks.json"
        self.manager = TaskManager(self.storage_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_and_list_task(self):
        task = self.manager.create_task("Reciclar papel", "Separar cartón y papel", "medium", "home")
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, task.id)
        self.assertEqual(tasks[0].impact, "medium")

    def test_update_task(self):
        task = self.manager.create_task("Ir al trabajo", "Usar transporte público", "high", "commute")
        updated = self.manager.update_task(task.id, title="Ir al trabajo en bici", impact="low", completed=True)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.title, "Ir al trabajo en bici")
        self.assertEqual(updated.impact, "low")
        self.assertTrue(updated.completed)

    def test_delete_task(self):
        task = self.manager.create_task("Reutilizar botella", "Llevar una botella de agua", "low", "daily")
        self.assertTrue(self.manager.delete_task(task.id))
        self.assertIsNone(self.manager.get_task(task.id))

    def test_report_and_suggestions(self):
        self.manager.create_task("Reciclar", "Separar plástico", "low", "home")
        self.manager.create_task("Viaje largo", "Ir a otra ciudad", "high", "travel")
        report = self.manager.generate_report(self.manager.list_tasks())
        self.assertEqual(report["total_tasks"], 2)
        self.assertEqual(report["carbon_footprint"], 6)
        suggestions = self.manager.eco_suggestions(self.manager.list_tasks())
        self.assertTrue(any("public transportation" in item.lower() for item in suggestions))

    def test_invalid_impact_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.create_task("Invalid task", "description", "extreme")


if __name__ == "__main__":
    unittest.main()

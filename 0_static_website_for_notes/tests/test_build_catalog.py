import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_catalog import catalog_files, write_catalog


class BuildCatalogTests(unittest.TestCase):
    def test_catalog_sorts_module_numbers_naturally_and_includes_supported_types(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for filename in (
                "Module 10.ipynb",
                "Module 2.docx",
                "Module 1.pptx",
                "notes.txt",
                "workbook.xlsx",
                ".secret.txt",
                "~$Module 3.docx",
            ):
                (root / filename).write_text("sample", encoding="utf-8")
            hidden_directory = root / ".hidden"
            hidden_directory.mkdir()
            (hidden_directory / "private.pdf").write_text("sample", encoding="utf-8")

            items = catalog_files(root)

        self.assertEqual(
            [item["name"] for item in items],
            ["Module 1.pptx", "Module 2.docx", "Module 10.ipynb", "notes.txt", "workbook.xlsx"],
        )
        self.assertEqual(
            [item["extension"] for item in items],
            [".pptx", ".docx", ".ipynb", ".txt", ".xlsx"],
        )
        names = [item["name"] for item in items]
        self.assertIn("workbook.xlsx", names)
        self.assertIn("notes.txt", names)
        self.assertNotIn(".secret.txt", names)
        self.assertNotIn("private.pdf", names)

    def test_nested_file_paths_are_relative_and_catalog_can_be_written(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "lessons"
            nested.mkdir()
            (nested / "Module 1.py").write_text("print('hello')", encoding="utf-8")
            output = root / "generated" / "catalog.json"

            count = write_catalog(root, output)

            self.assertEqual(count, 1)
            self.assertEqual(
                json.loads(output.read_text(encoding="utf-8")),
                [
                    {
                        "path": "lessons/Module 1.py",
                        "name": "Module 1.py",
                        "folder": "lessons",
                        "extension": ".py",
                    }
                ],
            )


if __name__ == "__main__":
    unittest.main()

"""Run only in the separately installed hosted V1 or V2 environment."""
import importlib.util
import os
from pathlib import Path
import sys
import unittest

import pydantic
from pydantic import ValidationError


LINE = os.environ.get("PYDANTIC_LINE")
PINS = {"1": "1.10.26", "2": "2.13.5"}
if LINE not in PINS or pydantic.__version__ != PINS[LINE]:
    raise RuntimeError("Set PYDANTIC_LINE=1 or 2 and install the matching pinned requirements")


def load_example(stem):
    path = Path(__file__).resolve().parents[1] / "examples" / f"v{LINE}" / f"{stem}.py"
    name = f"sample_v{LINE}_{stem}"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


items = load_example("item_validator")
defaults = load_example("default_validator")
exceptions = load_example("validation_exception")


class ItemValidatorTests(unittest.TestCase):
    def test_normalizes_each_valid_item(self):
        model = items.LabelSet(labels=["  alpha ", "beta"])
        self.assertEqual(model.labels, ["alpha", "beta"])

    def test_empty_item_is_rejected_at_its_index(self):
        with self.assertRaises(ValidationError) as caught:
            items.LabelSet(labels=["alpha", "   "])
        error = caught.exception.errors()[0]
        self.assertEqual(error["loc"], ("labels", 1))
        self.assertIn("label must contain visible text", error["msg"])

    def test_wrong_item_type_is_rejected_at_its_index(self):
        with self.assertRaises(ValidationError) as caught:
            items.LabelSet(labels=["alpha", None])
        self.assertEqual(caught.exception.errors()[0]["loc"], ("labels", 1))

    def test_empty_container_is_still_allowed(self):
        self.assertEqual(items.LabelSet(labels=[]).labels, [])


class DefaultValidatorTests(unittest.TestCase):
    def test_omitted_field_normalizes_the_explicit_default(self):
        self.assertEqual(defaults.Profile().display_name, "guest")

    def test_explicit_none_preserves_the_source_policy(self):
        self.assertEqual(defaults.Profile(display_name=None).display_name, "anonymous")

    def test_supplied_name_is_normalized(self):
        self.assertEqual(defaults.Profile(display_name="  Ada  ").display_name, "Ada")

    def test_empty_string_preserves_the_source_policy(self):
        self.assertEqual(defaults.Profile(display_name="").display_name, "anonymous")


class ValidationExceptionTests(unittest.TestCase):
    def test_valid_priority_is_preserved(self):
        self.assertEqual(exceptions.WorkItem(priority=3).priority, 3)

    def test_business_rule_remains_a_structured_validation_error(self):
        with self.assertRaises(ValidationError) as caught:
            exceptions.WorkItem(priority=11)
        error = caught.exception.errors()[0]
        self.assertEqual(error["loc"], ("priority",))
        self.assertEqual(error["type"], "type_error" if LINE == "1" else "value_error")
        self.assertIn("priority must be between 0 and 10", error["msg"])

    def test_core_type_validation_is_not_bypassed(self):
        with self.assertRaises(ValidationError) as caught:
            exceptions.WorkItem(priority="urgent")
        self.assertEqual(caught.exception.errors()[0]["loc"], ("priority",))

    def test_programming_type_error_has_the_documented_version_difference(self):
        expected = ValidationError if LINE == "1" else TypeError
        with self.assertRaises(expected):
            exceptions.ProgrammingErrorExample(count=3)


if __name__ == "__main__":
    unittest.main()

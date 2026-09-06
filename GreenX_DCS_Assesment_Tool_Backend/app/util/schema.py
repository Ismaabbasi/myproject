from typing import Optional

from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass


class AllOptional(ModelMetaclass):
    def __new__(mcs, name, bases, namespace, **kwargs):
        annotations = namespace.get("__annotations__", {}).copy()

        for base in bases:
            base_annotations = getattr(base, "__annotations__", {})
            annotations.update(base_annotations)

        for field_name, field_type in annotations.items():
            if not field_name.startswith("__"):
                annotations[field_name] = Optional[field_type]

        namespace["__annotations__"] = annotations

        return super().__new__(mcs, name, bases, namespace, **kwargs)

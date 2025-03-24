from dataclasses import dataclass, field


@dataclass
class Base:
    id: int | None = None
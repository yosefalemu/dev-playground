from dataclasses import dataclass
from typing import Optional

@dataclass
class ProductSearchFilters:
    name: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None


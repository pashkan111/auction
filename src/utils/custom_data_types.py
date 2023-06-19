from decimal import Decimal
from typing import Annotated

from pydantic import Field

PriceType = Annotated[Decimal, Field(gt=0, decimal_places=2)]

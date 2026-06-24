from pydantic import BaseModel
from pydantic import Field


class TransactionRequest(BaseModel):

    userId: str = Field(
        min_length=1
    )

    amount: float = Field(
        gt=0
    )

    transactionId: str = Field(
        min_length=1
    )
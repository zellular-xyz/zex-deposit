from datetime import datetime
from enum import Enum, auto
from typing import TypeAlias

from pydantic import BaseModel, Field
from eth_typing import URI, BlockNumber, ChainId, ChecksumAddress

Value: TypeAlias = int
Timestamp: TypeAlias = int | float
UserId: TypeAlias = int
TxHash: TypeAlias = str


class ChainConfig(BaseModel):
    private_rpc: URI | str
    chain_id: ChainId


class TransferStatus(Enum):
    PENDING = auto()
    FINALIZED = auto()
    VERIFIED = auto()
    REORG = auto()
    REJECTED = auto()


class RawTransfer(BaseModel):
    tx_hash: TxHash
    status: TransferStatus
    chain_id: ChainId
    value: Value
    token: ChecksumAddress
    to: ChecksumAddress
    observed_at: Timestamp = Field(default_factory=lambda: datetime.now().timestamp())
    block_number: BlockNumber

    class Config:
        use_enum_values = True


class ValidTransfer(RawTransfer):
    user_id: UserId

    class Config:
        use_enum_values = True


class UserAddress(BaseModel):
    user_id: UserId
    address: ChecksumAddress
    is_active: bool = Field(default=True)

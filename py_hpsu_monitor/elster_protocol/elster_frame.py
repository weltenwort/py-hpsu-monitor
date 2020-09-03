from typing import NamedTuple, Optional


class ElsterFrame(NamedTuple):
    sender: int
    receiver: int
    type: int
    elster_index: int
    value: Optional[int]

    def __str__(self):
        return (
            f"ElsterFrame("
            f"sender={self.sender:x}, "
            f"receiver={self.receiver:x}, "
            f"type={self.type}, "
            f"elster_index={self.elster_index:04x}, "
            f"value={self.value}"
            ")"
        )

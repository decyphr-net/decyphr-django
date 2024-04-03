from dataclasses import dataclass


@dataclass
class TextPiece:
    text_item: str
    pos_tag: str

import re

from typing import List, Optional
from pydantic import BaseModel, Field


class CleanRule(BaseModel):
    pattern: str = Field(...,
                         description="Regex pattern to search in the HTML")
    replacement: Optional[str] = Field(
        None,
        description="Replacement string for the matched pattern. If omitted, the text will be removed."
    )
    flags: Optional[List[str]] = Field(
        default=None,
        description="Optional regex flags (e.g. ['ignorecase', 'dotall'])"
    )

    def compile_flags(self) -> int:
        flag_map = {
            "ignorecase": re.IGNORECASE,
            "multiline": re.MULTILINE,
            "dotall": re.DOTALL,
        }
        result = 0
        if self.flags:
            for f in self.flags:
                result |= flag_map.get(f.lower(), 0)
        return result

    def apply(self, text: str) -> str:
        return re.sub(
            self.pattern,
            self.replacement if self.replacement is not None else "",
            text,
            flags=self.compile_flags()
        )

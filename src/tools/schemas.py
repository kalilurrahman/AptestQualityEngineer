from pydantic import BaseModel, Field
from typing import Optional, Literal

class InteractWithUIInput(BaseModel):
    action: Literal["click", "type", "hover", "navigate", "wait"] = Field(description="The action to perform on the UI element.")
    description: str = Field(description="Visual description of the element to interact with, e.g., 'The blue Submit button in the top right'. For 'navigate', this is the URL.")
    value: Optional[str] = Field(None, description="The value to type into the input field (for 'type' action) or wait time in seconds (for 'wait').")

class InteractWithUIOutput(BaseModel):
    success: bool
    message: str
    screenshot: Optional[str] = None
    dom_snapshot: Optional[str] = None

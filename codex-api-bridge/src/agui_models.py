"""AG-UI and history response models (mirrors langgraph-agent)."""
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ContentObject(BaseModel):
    """Content object for AG-UI messages."""
    type: str  # "text", "rich", "card", "table", "image", "attachments", "error"
    text: Optional[str] = None
    blocks: Optional[List[Dict]] = None
    columns: Optional[List[str]] = None
    rows: Optional[List[List[str]]] = None
    attachments: Optional[List[Dict]] = None


class AGUIMessage(BaseModel):
    """AG-UI message format."""
    id: str
    role: str  # "assistant", "system", "tool", "user"
    content: ContentObject


class Action(BaseModel):
    """Action for buttons/suggestions."""
    type: str
    label: str
    id: str
    payload: Optional[Dict] = None


class Metadata(BaseModel):
    """Metadata for AG-UI response."""
    user_id: str
    thread_id: str
    agent_type: str
    project_id: Optional[str] = None
    project_name: Optional[str] = None


class AGUIResponse(BaseModel):
    """AG-UI compatible response format."""
    id: str
    type: str = "response"
    created_at: str  # ISO timestamp
    status: str  # "ok", "partial", "error"
    messages: List[AGUIMessage]
    actions: Optional[List[Action]] = None
    metadata: Metadata


class AGUIDelta(BaseModel):
    """AG-UI streaming delta format."""
    type: str  # "delta" or "done"
    response_id: str
    message_id: Optional[str] = None
    content: Optional[Dict] = None


class HistoryResponse(BaseModel):
    """History response in OpenAI-style message format."""
    messages: List[Dict[str, Any]]
    user_id: str
    thread_id: str
    message_count: int
    chat_name: str = "New Chat"
    agent_type: str = "codex"
    project_id: Optional[str] = None
    project_name: Optional[str] = None
    usage_metadata: Optional[Dict[str, Any]] = None

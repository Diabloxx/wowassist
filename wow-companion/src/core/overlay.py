"""Overlay rendering integration wrapper."""
from __future__ import annotations
from .reasoner import ActionDecision
from ..config import config
from rich.console import Console
from rich.panel import Panel
import time

console = Console()
_last_render = 0.0

def render(decision: ActionDecision, state):
    global _last_render
    if time.time() - _last_render < 0.1:
        return
    label = "ASSIST" if config.ASSIST_MODE else ("AUTO" if config.AUTOMATION_MODE else "ASSIST")
    banner = f"[bold red]AUTOMATION ON[/bold red]" if config.AUTOMATION_MODE else ""
    console.clear()
    console.print(Panel.fit(f"{banner}\n[bold cyan]{decision.action}[/bold cyan]\nprio={decision.priority:.2f} horizon={decision.horizon_ms}ms\n{decision.rationale}", title=label))
    _last_render = time.time()

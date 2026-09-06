import argparse
from typing import Sequence

from pydantic import BaseModel, Field


class CLIArgs(BaseModel):
    """Command-line arguments for the Bonfire server."""

    port: int = Field(default=5000, description="Server port")
    debug: bool = Field(default=False, description="Debug mode")

    @classmethod
    def parse(cls, args: Sequence[str] | None = None) -> "CLIArgs":
        parser = argparse.ArgumentParser(description="Bonfire Backend Server")
        parser.add_argument("--debug", action="store_true", help="Debug mode")
        parser.add_argument("--port", type=int, default=5000, help="Server port")
        parsed = parser.parse_args(args)
        return cls.model_validate(vars(parsed))


# Backward compatibility alias
BonfireArgumentParser = CLIArgs.parse

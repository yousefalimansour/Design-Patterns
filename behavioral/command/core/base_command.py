"""
Base Command class for Command Pattern implementation.

This module defines the abstract base class that all concrete commands must inherit from.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)


class BaseCommand(ABC):
    """
    Abstract base class for all commands in the system.
    
    Commands encapsulate a request as an object, allowing for parameterization
    of clients with different requests, queuing of requests, and logging of operations.
    
    Attributes:
        result: Stores the result of command execution
        executed: Flag indicating whether the command has been executed
    """
    
    def __init__(self):
        """Initialize the command with default state."""
        self.result: Optional[Any] = None
        self.executed: bool = False
    
    @abstractmethod
    def execute(self) -> Any:
        """
        Execute the command and perform the requested operation.
        
        This method must be implemented by all concrete command classes.
        
        Returns:
            Any: The result of the command execution
            
        Raises:
            Exception: If the command execution fails
        """
        pass
    
    def undo(self) -> Any:
        """
        Undo the command operation if possible.
        
        Default implementation does nothing. Override in concrete commands
        that support undo functionality.
        
        Returns:
            Any: The result of the undo operation
        """
        logger.warning(f"{self.__class__.__name__} does not support undo operation")
        return None
    
    def can_undo(self) -> bool:
        """
        Check if this command can be undone.
        
        Returns:
            bool: True if the command can be undone, False otherwise
        """
        return False
    
    def __str__(self) -> str:
        """String representation of the command."""
        return f"{self.__class__.__name__}(executed={self.executed})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the command."""
        return f"{self.__class__.__name__}(executed={self.executed}, result={self.result})"

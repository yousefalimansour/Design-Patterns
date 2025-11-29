"""
Command Invoker for managing and executing commands.

The invoker is responsible for executing commands, maintaining command history,
and providing undo functionality.
"""

from typing import List, Optional, Any
import logging
from .base_command import BaseCommand

logger = logging.getLogger(__name__)


class CommandInvoker:
    """
    The Invoker class is responsible for executing commands.
    
    It maintains a history of executed commands and provides functionality
    to undo previously executed commands.
    
    Attributes:
        history: List of executed commands
        max_history_size: Maximum number of commands to keep in history
    """
    
    def __init__(self, max_history_size: int = 100):
        """
        Initialize the CommandInvoker.
        
        Args:
            max_history_size: Maximum number of commands to keep in history (default: 100)
        """
        self.history: List[BaseCommand] = []
        self.max_history_size = max_history_size
    
    def execute_command(self, command: BaseCommand) -> Any:
        """
        Execute a command and add it to the history.
        
        Args:
            command: The command to execute
            
        Returns:
            Any: The result of the command execution
            
        Raises:
            Exception: If command execution fails
        """
        try:
            logger.info(f"Executing command: {command}")
            result = command.execute()
            command.executed = True
            command.result = result
            
            # Add to history
            self.history.append(command)
            
            # Maintain history size limit
            if len(self.history) > self.max_history_size:
                self.history.pop(0)
            
            logger.info(f"Command executed successfully: {command}")
            return result
            
        except Exception as e:
            logger.error(f"Command execution failed: {command}. Error: {str(e)}")
            raise
    
    def undo_last_command(self) -> Optional[Any]:
        """
        Undo the last executed command if it supports undo.
        
        Returns:
            Optional[Any]: The result of the undo operation, or None if no command to undo
            
        Raises:
            ValueError: If the last command doesn't support undo
        """
        if not self.history:
            logger.warning("No commands to undo")
            return None
        
        command = self.history[-1]
        
        if not command.can_undo():
            raise ValueError(f"Command {command} does not support undo operation")
        
        try:
            logger.info(f"Undoing command: {command}")
            result = command.undo()
            self.history.pop()
            logger.info(f"Command undone successfully: {command}")
            return result
            
        except Exception as e:
            logger.error(f"Command undo failed: {command}. Error: {str(e)}")
            raise
    
    def get_history(self) -> List[BaseCommand]:
        """
        Get the command execution history.
        
        Returns:
            List[BaseCommand]: List of executed commands
        """
        return self.history.copy()
    
    def clear_history(self) -> None:
        """Clear the command execution history."""
        self.history.clear()
        logger.info("Command history cleared")
    
    def __str__(self) -> str:
        """String representation of the invoker."""
        return f"CommandInvoker(history_size={len(self.history)})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the invoker."""
        return f"CommandInvoker(history_size={len(self.history)}, max_history_size={self.max_history_size})"

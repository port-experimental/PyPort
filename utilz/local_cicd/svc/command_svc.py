"""
Command service for local CI/CD utilities.

This module provides a command pattern implementation for CI/CD tasks.
"""
import abc
from typing import Any, Dict, List, Optional, Tuple, Union

from utilz.local_cicd.cfg.cicd_cfg import CicdConfig
from utilz.local_cicd.svc.logging_svc import get_logger


class Command(abc.ABC):
    """
    Abstract base class for commands.
    
    Commands encapsulate a specific CI/CD task and provide a consistent
    interface for executing and undoing the task.
    """
    
    def __init__(self, config: CicdConfig, name: str = None):
        """
        Initialize the command.
        
        Args:
            config: Configuration for the CI/CD utilities.
            name: Name of the command (defaults to the class name).
        """
        self.config = config
        self.name = name or self.__class__.__name__
        self.logger = get_logger(f"command.{self.name.lower()}")
        self.result = None
    
    @abc.abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute the command.
        
        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
            
        Returns:
            The result of the command execution.
        """
        pass
    
    def undo(self) -> bool:
        """
        Undo the command.
        
        Returns:
            True if the command was successfully undone, False otherwise.
        """
        self.logger.warning(f"Undo not implemented for {self.name}")
        return False
    
    def can_undo(self) -> bool:
        """
        Check if the command can be undone.
        
        Returns:
            True if the command can be undone, False otherwise.
        """
        return False


class CommandInvoker:
    """
    Invoker for commands.
    
    The invoker is responsible for executing commands and maintaining
    a history of executed commands.
    """
    
    def __init__(self):
        """Initialize the command invoker."""
        self.history: List[Command] = []
        self.logger = get_logger("command.invoker")
    
    def execute(self, command: Command, *args, **kwargs) -> Any:
        """
        Execute a command and add it to the history.
        
        Args:
            command: Command to execute.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
            
        Returns:
            The result of the command execution.
        """
        self.logger.info(f"Executing command: {command.name}")
        result = command.execute(*args, **kwargs)
        command.result = result
        self.history.append(command)
        return result
    
    def undo_last(self) -> bool:
        """
        Undo the last command.
        
        Returns:
            True if the command was successfully undone, False otherwise.
        """
        if not self.history:
            self.logger.warning("No commands to undo")
            return False
        
        command = self.history.pop()
        self.logger.info(f"Undoing command: {command.name}")
        
        if not command.can_undo():
            self.logger.warning(f"Command {command.name} cannot be undone")
            return False
        
        return command.undo()
    
    def undo_all(self) -> bool:
        """
        Undo all commands in reverse order.
        
        Returns:
            True if all commands were successfully undone, False otherwise.
        """
        success = True
        while self.history:
            if not self.undo_last():
                success = False
        return success
    
    def clear_history(self) -> None:
        """Clear the command history."""
        self.history = []
    
    def get_history(self) -> List[Tuple[str, Any]]:
        """
        Get the command history.
        
        Returns:
            A list of tuples containing the command name and result.
        """
        return [(command.name, command.result) for command in self.history]


class CommandFactory:
    """
    Factory for creating commands.
    
    The factory is responsible for creating commands based on their name
    and providing a registry of available commands.
    """
    
    _registry: Dict[str, type] = {}
    
    @classmethod
    def register(cls, command_class: type) -> type:
        """
        Register a command class.
        
        Args:
            command_class: Command class to register.
            
        Returns:
            The registered command class.
        """
        cls._registry[command_class.__name__] = command_class
        return command_class
    
    @classmethod
    def create(cls, name: str, config: CicdConfig, **kwargs) -> Command:
        """
        Create a command by name.
        
        Args:
            name: Name of the command.
            config: Configuration for the CI/CD utilities.
            **kwargs: Additional keyword arguments.
            
        Returns:
            A command instance.
            
        Raises:
            ValueError: If the command is not registered.
        """
        if name not in cls._registry:
            raise ValueError(f"Command not registered: {name}")
        
        command_class = cls._registry[name]
        return command_class(config, **kwargs)
    
    @classmethod
    def get_available_commands(cls) -> List[str]:
        """
        Get a list of available commands.
        
        Returns:
            A list of command names.
        """
        return list(cls._registry.keys())


# Decorator for registering commands
def register_command(cls):
    """
    Decorator for registering commands.
    
    Args:
        cls: Command class to register.
        
    Returns:
        The registered command class.
    """
    return CommandFactory.register(cls)

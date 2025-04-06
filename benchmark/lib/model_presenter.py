from typing import Optional
from pathlib import Path
from enum import Enum, auto
import logging

class OutputFormat(Enum):
    """Supported output formats"""
    PLAIN = auto()
    VERBOSE = auto()

class SMT2ModelPresenter:
    """Handles rich presentation of model information for CLI output"""
    
    def __init__(self, model):
        self.model = model
        self.stats = None
        self.logger = logging.getLogger("bt.model_presenter")
    
    def show(self, 
             verbose: bool = False,
             format: OutputFormat = OutputFormat.PLAIN,
             output_file: Optional[Path] = None):
        """
        Display model information in specified format
        
        Args:
            verbose: Show detailed information
            format: Output format (PLAIN, VERBOSE)
            output_file: Optional file to write output to
        """
        self.stats = self.model.parser.parse()
        
        output = self._generate_output(format, verbose)
        
        if output_file:
            self._write_output(output, output_file)
        else:
            self.logger.info(output)
    
    def _generate_output(self, format: OutputFormat, verbose: bool) -> str:
        """Generate formatted output string"""
        if format == OutputFormat.VERBOSE:
            return self._generate_verbose()
        elif format == OutputFormat.PLAIN:
            return self._generate_plain(verbose)
    
    def _generate_plain(self, verbose: bool) -> str:
        """Generate plain text output"""
        lines = [
            f"Model: {self.model.output_path.name}",
            f"Type: {self.model.__class__.__name__}",
            f"Code lines: {self.stats['code_lines']}",
        ]
        
        if verbose:
            lines.extend([
                "",
                "Detailed Analysis:",
                f"Total lines: {self.stats['total_lines']}",
                f"Comments: {self.stats['comment_lines']}",
                f"Blank lines: {self.stats['blank_lines']}",
                f"Define-fun commands: {self.stats['define_count']}",
            ])
            
            if self.stats['is_rotor_generated']:
                lines.append("\nRotor Configuration:")
                lines.extend(self._format_rotor_info())
        
        return "\n".join(lines)
    
    def _generate_verbose(self) -> str:
        """Generate rich verbose output with borders"""
        width = 70
        header = f" MODEL ANALYSIS ".center(width, "=")
        footer = "=" * width
        
        sections = [
            self._section("Basic Info", [
                f"File: {self.model.output_path.name}",
                f"Path: {self.model.output_path.resolve()}",
                f"Type: {self.model.__class__.__name__}",
            ]),
            
            self._section("Statistics", [
                f"Total lines: {self.stats['total_lines']}",
                f"Code lines: {self.stats['code_lines']}",
                f"Comments: {self.stats['comment_lines']}",
                f"Blank lines: {self.stats['blank_lines']}",
                f"Define-fun commands: {self.stats['define_count']}",
            ]),
        ]
        
        if self.stats['is_rotor_generated']:
            sections.append(
                self._section("Rotor Configuration", self._format_rotor_info())
            )
        
        return f"\n{header}\n" + "\n\n".join(sections) + f"\n{footer}\n"
    
    def _format_rotor_info(self) -> list[str]:
        """Format Rotor-specific information"""
        header = self.stats['rotor_header']
        return [
            f"Source: {header.source_file}",
            f"kMin: {header.kmin}, kMax: {header.kmax}",
            f"Virtual Address Space: {header.virtual_address_space}-bit",
            f"Code Size: {header.bytecode_size} bytes",
            f"Data Size: {header.data_size} bytes",
            f"Flags: {', '.join(header.flags) if header.flags else 'None'}",
        ]
    
    @staticmethod
    def _section(title: str, items: list[str]) -> str:
        """Create a bordered section"""
        lines = [f" {title} ".center(40, "-")]
        lines.extend(items)
        return "\n".join(lines)
    
    @staticmethod
    def _write_output(content: str, path: Path):
        """Write output to file"""
        with open(path, 'w') as f:
            f.write(content)
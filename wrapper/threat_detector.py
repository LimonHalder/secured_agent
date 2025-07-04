"""
Threat Detection Module

This module provides mechanisms to:
- Load threat patterns from a YAML configuration file
- Compile regex patterns
- Scan input/output text for known threats
- Block critical threats and log incidents

Author: Limon Halder
"""

import re
import yaml
from typing import Dict, List, Pattern

from logger.logger import log_threat


def load_threat_patterns_from_yaml(
    path: str = "wrapper/config.yml",
) -> Dict[str, List[str]]:
    """
    Load raw threat patterns from a YAML file.

    Args:
        path (str): Path to the YAML file.

    Returns:
        Dict[str, List[str]]: A dictionary of threat categories and their associated regex strings.
    """
    try:
        with open(path, "r") as file:
            patterns = yaml.safe_load(file)
        if not isinstance(patterns, dict):
            print(f"⚠️ Warning: Expected dict from YAML, got {type(patterns)}")
            return {}
        return patterns
    except Exception as e:
        print(f"⚠️ Warning: Failed to load threat patterns from '{path}': {e}")
        return {}


def compile_threat_patterns(
    raw_patterns: Dict[str, List[str]]
) -> Dict[str, List[Pattern]]:
    """
    Compile raw regex strings into regex Pattern objects.

    Args:
        raw_patterns (Dict[str, List[str]]): Raw threat patterns loaded from YAML.

    Returns:
        Dict[str, List[Pattern]]: Compiled regex patterns per threat type.
    """
    compiled: Dict[str, List[Pattern]] = {}

    for threat_name, patterns in raw_patterns.items():
        compiled[threat_name] = []
        if isinstance(patterns, list):
            for p in patterns:
                try:
                    compiled_pattern = re.compile(p, re.IGNORECASE)
                    compiled[threat_name].append(compiled_pattern)
                except re.error as e:
                    print(
                        f"⚠️ Warning: Invalid regex pattern '{p}' for threat "
                        f"'{threat_name}': {e}"
                    )
        else:
            print(
                f"⚠️ Warning: Patterns for threat '{threat_name}' should be a list, "
                f"got {type(patterns)}"
            )

    return compiled


# Load and compile threat patterns on module load
RAW_THREAT_PATTERNS: Dict[str, List[str]] = load_threat_patterns_from_yaml()
THREAT_PATTERNS: Dict[str, List[Pattern]] = compile_threat_patterns(RAW_THREAT_PATTERNS)


def check_for_threats(text: str, stage: str = "input") -> bool:
    """
    Check the given text for known threat patterns.

    Args:
        text (str): The text to analyze.
        stage (str): Either "input" or "output", used for logging context.

    Returns:
        bool: False if critical threat is found (should block), True otherwise.
    """
    if not isinstance(text, str):
        text = str(text) if text is not None else ""

    threats_found: List[str] = []

    for threat_name, patterns in THREAT_PATTERNS.items():
        for pattern in patterns:
            if pattern.search(text):
                threats_found.append(threat_name)
                break  # Stop checking more patterns in this threat category

    for threat in threats_found:
        log_threat(threat, text, stage)

    # These are considered severe and should block message
    critical_threats = {
        "Prompt Injection",
        "Data Exfiltration",
        "Social Engineering",
        "Unauthorized Access",
    }

    return not any(threat in critical_threats for threat in threats_found)

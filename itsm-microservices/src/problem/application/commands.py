from dataclasses import dataclass
from typing import Optional, List


@dataclass
class CreateProblemCommand:
  title: str
  description: str
  created_by: str


@dataclass
class StartRCACommand:
  problem_id: str


@dataclass
class CompleteRCACommand:
  problem_id: str
  root_cause: str


@dataclass
class ResolveProblemCommand:
  problem_id: str


@dataclass
class AddRelatedIncidentCommand:
  problem_id: str
  incident_id: str


@dataclass
class AddImpactedServiceCommand:
  problem_id: str
  service_name: str


@dataclass
class CreateKnownErrorCommand:
  problem_id: str
  workaround: str
  temporary_fix: str
  permanent_fix: str


@dataclass
class DeactivateKnownErrorCommand:
  known_error_id: str

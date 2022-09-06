from dataclasses import dataclass, field
from typing import Sequence

from common.credentials import Credentials

from . import AbstractAgentEvent


@dataclass(frozen=True)
class CredentialsStolenEvent(AbstractAgentEvent):
    """
    An event that occurs when an agent collects credentials from the victim

    Attributes:
        :param stolen_credentials: The credentials that were stolen by an agent
    """

    stolen_credentials: Sequence[Credentials] = field(default_factory=list)

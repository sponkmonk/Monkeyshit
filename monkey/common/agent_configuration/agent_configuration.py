from typing import Tuple

from pydantic import Field, confloat

from common.base_models import MutableInfectionMonkeyBaseModel

from .agent_sub_configurations import PluginConfiguration, PropagationConfiguration


class AgentConfiguration(MutableInfectionMonkeyBaseModel):
    keep_tunnel_open_time: confloat(ge=0) = Field(  # type: ignore[valid-type]
        title="Keep tunnel open time",
        description="Time to keep tunnel open before "
        "going down after last exploit (in "
        "seconds)",
        default=30,
    )
    credential_collectors: Tuple[PluginConfiguration, ...] = Field(title="Credential collectors")
    payloads: Tuple[PluginConfiguration, ...] = Field(title="Payloads")
    propagation: PropagationConfiguration = Field(title="Propagation")

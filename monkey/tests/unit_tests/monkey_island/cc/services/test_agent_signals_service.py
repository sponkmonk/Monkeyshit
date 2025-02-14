from unittest.mock import MagicMock
from uuid import UUID

import pytest

from common.types import AgentID
from monkey_island.cc.models import Agent, IslandMode, Simulation, TerminateAllAgents
from monkey_island.cc.repositories import (
    IAgentRepository,
    ISimulationRepository,
    UnknownRecordError,
)
from monkey_island.cc.services import AgentSignalsService

AGENT_1 = Agent(
    id=UUID("f811ad00-5a68-4437-bd51-7b5cc1768ad5"),
    machine_id=1,
    start_time=100,
    parent_id=None,
)

AGENT_2 = Agent(
    id=UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10"),
    machine_id=2,
    start_time=200,
    parent_id=AGENT_1.id,
)

AGENT_3 = Agent(
    id=UUID("0fc9afcb-1902-436b-bd5c-1ad194252484"),
    machine_id=3,
    start_time=300,
    parent_id=AGENT_2.id,
)

AGENTS = [AGENT_1, AGENT_2, AGENT_3]

STOPPED_AGENT = Agent(
    id=UUID("e810ad01-6b67-9446-fc58-9b8d717653f7"),
    machine_id=4,
    start_time=400,
    stop_time=500,
    parent_id=AGENT_3.id,
)

ALL_AGENTS = [*AGENTS, STOPPED_AGENT]


@pytest.fixture
def mock_simulation_repository() -> IAgentRepository:
    return MagicMock(spec=ISimulationRepository)


@pytest.fixture(scope="session")
def mock_agent_repository() -> IAgentRepository:
    def get_agent_by_id(agent_id: AgentID) -> Agent:
        for agent in ALL_AGENTS:
            if agent.id == agent_id:
                return agent

        raise UnknownRecordError(str(agent_id))

    agent_repository = MagicMock(spec=IAgentRepository)
    agent_repository.get_progenitor = MagicMock(return_value=AGENT_1)
    agent_repository.get_agent_by_id = MagicMock(side_effect=get_agent_by_id)

    return agent_repository


@pytest.fixture
def agent_signals_service(mock_simulation_repository, mock_agent_repository) -> AgentSignalsService:
    return AgentSignalsService(mock_simulation_repository, mock_agent_repository)


def test_stopped_agent(
    agent_signals_service: AgentSignalsService,
    mock_simulation_repository: ISimulationRepository,
):
    agent = STOPPED_AGENT
    mock_simulation_repository.get_simulation = MagicMock(
        return_value=Simulation(terminate_signal_time=None)
    )

    signals = agent_signals_service.get_signals(agent.id)
    assert signals.terminate == agent.stop_time


@pytest.mark.parametrize("agent", AGENTS)
def test_terminate_is_none(
    agent,
    agent_signals_service: AgentSignalsService,
    mock_simulation_repository: ISimulationRepository,
):
    mock_simulation_repository.get_simulation = MagicMock(
        return_value=Simulation(terminate_signal_time=None)
    )

    signals = agent_signals_service.get_signals(agent.id)
    assert signals.terminate is None


@pytest.mark.parametrize("agent", AGENTS)
def test_agent_started_before_terminate(
    agent,
    agent_signals_service: AgentSignalsService,
    mock_simulation_repository: ISimulationRepository,
):
    TERMINATE_TIMESTAMP = 400
    mock_simulation_repository.get_simulation = MagicMock(
        return_value=Simulation(terminate_signal_time=TERMINATE_TIMESTAMP)
    )

    signals = agent_signals_service.get_signals(agent.id)

    assert signals.terminate.timestamp() == TERMINATE_TIMESTAMP


@pytest.mark.parametrize("agent", AGENTS)
def test_agent_started_after_terminate(
    agent,
    agent_signals_service: AgentSignalsService,
    mock_simulation_repository: ISimulationRepository,
):
    TERMINATE_TIMESTAMP = 50
    mock_simulation_repository.get_simulation = MagicMock(
        return_value=Simulation(terminate_signal_time=TERMINATE_TIMESTAMP)
    )

    signals = agent_signals_service.get_signals(agent.id)

    assert signals.terminate is None


@pytest.mark.parametrize("agent", AGENTS)
def test_progenitor_started_before_terminate(
    agent,
    agent_signals_service: AgentSignalsService,
    mock_simulation_repository: ISimulationRepository,
):
    TERMINATE_TIMESTAMP = 150
    mock_simulation_repository.get_simulation = MagicMock(
        return_value=Simulation(terminate_signal_time=TERMINATE_TIMESTAMP)
    )

    signals = agent_signals_service.get_signals(agent.id)

    assert signals.terminate.timestamp() == TERMINATE_TIMESTAMP


def test_on_terminate_agents_signal__stores_timestamp(
    agent_signals_service: AgentSignalsService, mock_simulation_repository: ISimulationRepository
):
    timestamp = 100

    terminate_all_agents = TerminateAllAgents(timestamp=timestamp)
    mock_simulation_repository.get_simulation = MagicMock(return_value=Simulation())
    agent_signals_service.on_terminate_agents_signal(terminate_all_agents)

    expected_value = Simulation(terminate_signal_time=timestamp)
    assert mock_simulation_repository.save_simulation.called_once_with(expected_value)


def test_on_terminate_agents_signal__updates_timestamp(
    agent_signals_service: AgentSignalsService, mock_simulation_repository: ISimulationRepository
):
    timestamp = 100

    terminate_all_agents = TerminateAllAgents(timestamp=timestamp)
    mock_simulation_repository.get_simulation = MagicMock(
        return_value=Simulation(mode=IslandMode.RANSOMWARE, terminate_signal_time=50)
    )

    agent_signals_service.on_terminate_agents_signal(terminate_all_agents)

    expected_value = Simulation(mode=IslandMode.RANSOMWARE, terminate_signal_time=timestamp)
    assert mock_simulation_repository.save_simulation.called_once_with(expected_value)

import datetime

from omnim.src.events import EventType
from omnim.src.metrics.deployment_frequency import DeploymentFrequencyMetricCalculator
from omnim.src.metrics.leadtime import WorkflowEvent


class TestDeploymentFrequencyCalculator:
    def test_it_should_return_no_frequency_with_no_events(self):

        metric = DeploymentFrequencyMetricCalculator()

        result = metric.calculate([])

        assert result.deployment_frequency is None

    def test_it_should_return_no_frequency_with_no_deployment_success_event(
        self,
    ):  # noqa: E501

        metric = DeploymentFrequencyMetricCalculator()
        today = datetime.datetime.today()

        events_stream = (WorkflowEvent(today, EventType.BUILD_SUCCESS),)

        result = metric.calculate(events_stream)

        assert result.deployment_frequency is None

    def test_it_should_return_deployment_frequency_of_one(self):

        metric = DeploymentFrequencyMetricCalculator()
        today = datetime.datetime.today()

        events_stream = (
            WorkflowEvent(today, EventType.BUILD_SUCCESS),
            WorkflowEvent(today, EventType.DEPLOY_SUCCESS),
        )

        result = metric.calculate(events_stream)

        assert result.deployment_frequency == 1.0

    def test_it_should_return_deployment_frequency_of_0_5(self):

        metric = DeploymentFrequencyMetricCalculator()
        today = datetime.datetime.today()
        yesterday = today - datetime.timedelta(days=2)

        events_stream = (
            WorkflowEvent(yesterday, EventType.BUILD_FAILED),
            WorkflowEvent(today, EventType.DEPLOY_SUCCESS),
        )

        result = metric.calculate(events_stream)

        assert result.deployment_frequency == 0.5

    def test_it_should_return_deployment_frequency_of_0_666_for_two_success_deployments_in_3_days(  # noqa: E501
        self,
    ):

        metric = DeploymentFrequencyMetricCalculator()
        today = datetime.datetime.today()
        yesterday = today - datetime.timedelta(days=2)
        day_before = today - datetime.timedelta(days=3)

        events_stream = (
            WorkflowEvent(day_before, EventType.BUILD_FAILED),
            WorkflowEvent(yesterday, EventType.BUILD_FAILED),
            WorkflowEvent(today, EventType.DEPLOY_SUCCESS),
            WorkflowEvent(today, EventType.DEPLOY_SUCCESS),
        )

        result = metric.calculate(events_stream)

        assert result.deployment_frequency == 2 / 3

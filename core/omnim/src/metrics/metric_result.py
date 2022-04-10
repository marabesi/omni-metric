from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional

from pydantic import BaseModel


class MetricResult(ABC):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError("Metric result not implemented yet")

    def report(self) -> None:
        print(self)


class UnknownMetricResult(MetricResult):
    def __str__(self):
        return "General unspecific metric. No result possible"


class DeployFrequencyMetricResult(BaseModel, MetricResult):
    deployment_frequency: Optional[float]

    def __str__(self) -> str:
        if self.deployment_frequency is None:
            return (
                "This metric returned an empty value. "
                "It is likely that there was not enough information to compute it"
            )

        return f"Average Deployment Frequency = {self.deployment_frequency} dep/day"


class ChangeFailureRateMetricResult(BaseModel, MetricResult):
    change_failure_rate: Optional[float]

    def __str__(self) -> str:
        if self.change_failure_rate is None:
            return (
                "This metric returned an empty value. "
                "It is likely that there was not enough information to compute it"
            )

        return f"Average Change Failure Rate = {self.change_failure_rate} failures/dep"


class MeanTimeToRestoreMetricResult(BaseModel, MetricResult):
    mean_time_to_restore: Optional[float]

    def __str__(self) -> str:
        if self.mean_time_to_restore is None:
            return (
                "This metric returned an empty value. "
                "It is likely that there was not enough information to compute it"
            )

        return f"Mean Time To Restore = {self.mean_time_to_restore} second(s)"


class LeadtimeMetricResult(BaseModel, MetricResult):
    lead_time: Optional[timedelta]

    def __str__(self) -> str:
        if self.lead_time is None:
            return (
                "This metric returned an empty value. "
                "It is likely that there was not enough information to compute it"
            )
        else:
            return (
                "Average Build to Deploy Leadtime "
                f"= {self.lead_time.total_seconds()} s"
            )

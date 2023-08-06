import os
import platform

from abc import abstractmethod, ABCMeta

import requests
from django.conf import settings
from remo_app.version import __version__


class Payload(metaclass=ABCMeta):
    @abstractmethod
    def to_dict(self):
        raise NotImplementedError()

    def timestamp(self, timestamp) -> str:
        if not timestamp:
            return None
        return timestamp.isoformat()


class InstallationData(Payload):
    def __init__(self, conda_version='N/A', successful=False, finished=False):
        self.uuid = os.getenv('REMO_UUID', 'undefined')
        self.version = __version__
        self.platform = platform.platform()
        self.python = platform.python_version()
        self.conda = conda_version
        self.successful = successful
        self.finished = finished

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'version': self.version,
            'platform': self.platform,
            'python': self.python,
            'conda': self.conda,
            'successful': self.successful,
            'finished': self.finished,
        }


class StatsData(Payload):
    def __init__(self, srv_id: str, n_datasets: int, dataset_stats=[], annotation_set_stats=[]):
        self.uuid = os.getenv('REMO_UUID', 'undefined')
        self.srv_id = srv_id
        self.n_datasets = n_datasets
        self.dataset_stats = dataset_stats
        self.annotation_set_stats = annotation_set_stats

    def to_dict(self):
        return {
            'srv_id': self.srv_id,
            'uuid': self.uuid,
            'n_datasets': self.n_datasets,
            'dataset_stats': self.dataset_stats,
            'annotation_set_stats': self.annotation_set_stats,
        }


class UsageData(Payload):
    def __init__(self, srv_id: str, version: str, started_at, n_checks: int, last_check_at=None, stopped_at=None):
        self.uuid = os.getenv('REMO_UUID', 'undefined')
        self.srv_id = srv_id
        self.version = version
        self.started_at = started_at
        self.stopped_at = stopped_at
        self.last_check_at = last_check_at
        self.n_checks = n_checks

    def to_dict(self):
        return {
            'srv_id': self.srv_id,
            'uuid': self.uuid,
            'version': self.version,
            'started_at': self.timestamp(self.started_at),
            'stopped_at': self.timestamp(self.stopped_at),
            'last_check_at': self.timestamp(self.last_check_at),
            'n_checks': self.n_checks,
        }


class Stats:
    @staticmethod
    def _send_request(endpoint: str, payload: Payload) -> bool:
        url = f'{settings.REMO_STATS_SERVER}/api/v1/ui/aggregate/1/{endpoint}/'
        # print('URL:', url)
        # print('payload:', payload.to_dict())
        try:
            resp = requests.post(url=url, json=payload.to_dict(), timeout=2)
            # print('status:', resp.status_code)
            return resp.status_code == 200
        except Exception as err:
            pass
            # print('ERR:', err)
        return False

    @staticmethod
    def _send_installation_info(payload: Payload) -> bool:
        return Stats._send_request('installations', payload)

    @staticmethod
    def send_stats_info(srv_id: str, n_datasets: int, dataset_stats=[], annotation_set_stats=[]) -> bool:
        return Stats._send_request('stats', StatsData(srv_id, n_datasets, dataset_stats, annotation_set_stats))

    @staticmethod
    def send_usage_info(srv_id: str, version: str, started_at, n_checks: int, last_check_at=None, stopped_at=None) -> bool:
        return Stats._send_request('usage', UsageData(srv_id, version, started_at, n_checks, last_check_at=last_check_at, stopped_at=stopped_at))

    @staticmethod
    def start_installation(conda_version: str):
        Stats._send_installation_info(InstallationData(conda_version))

    @staticmethod
    def finish_installation(conda_version, successful=False):
        Stats._send_installation_info(InstallationData(conda_version, finished=True, successful=successful))

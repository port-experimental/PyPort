import os
from pathlib import Path


class CicdConfig(object):
    def __init__(self):
        self._dir_depth = 3
        self.project_root = Path(__file__).resolve().parents[self._dir_depth]
        self.src_folder = os.path.join(self.project_root, 'src')
        self.config_folder = os.path.dirname(os.path.abspath(__file__))
        self.coverage_config_file = os.path.join(self.config_folder, '.coveragerc')
        self.coverage_data_file = os.path.join(self.project_root, '.coverage')
        self.qchecks_config_file = os.path.join(self.config_folder, 'quality_checks.ini')
        self.coverage_badge_pattern: str = r'!\[Coverage\]\(.*\)'
        self.maintainability_badge_pattern: str = r'!\[Maintainability\]\(.*\)'
        self.security_badge_pattern: str = r'!\[Security\]\(.*\)'
        self.dependencies_badge_pattern: str = r'!\[Dependencies\]\(.*\)'
        self.pypi_repo_config_file = os.path.join(self.config_folder, '.pypirc')

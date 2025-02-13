from typing import Dict, List
from pyport.models.api_category import BaseResource


class Audit(BaseResource):
    """Audit API category for retrieving audit logs."""

    def get_audit_logs(self) -> List[Dict]:
        """
        Retrieve all audit logs.

        :return: A list of audit log dictionaries.
        """
        response = self._client.make_request("GET", "audit")
        return response.json().get("audits", [])

    def get_audit_log(self, audit_id: str) -> Dict:
        """
        Retrieve details for a specific audit log.

        :param audit_id: The identifier of the audit log.
        :return: A dictionary representing the audit log.
        """
        response = self._client.make_request("GET", f"audit/{audit_id}")
        return response.json().get("audit", {})

"""Unit tests for DMARC Monitoring resource."""

import pytest
from unittest.mock import Mock, MagicMock

from mailersend.resources.dmarc_monitoring import DmarcMonitoring
from mailersend.models.base import APIResponse
from mailersend.models.dmarc_monitoring import (
    DmarcMonitoringListRequest,
    DmarcMonitoringListQueryParams,
    DmarcMonitoringCreateRequest,
    DmarcMonitoringUpdateRequest,
    DmarcMonitoringDeleteRequest,
    DmarcMonitoringReportRequest,
    DmarcMonitoringReportQueryParams,
    DmarcMonitoringIpReportRequest,
    DmarcMonitoringReportSourcesRequest,
    DmarcMonitoringFavoriteRequest,
)


class TestDmarcMonitoringInit:
    """Test DmarcMonitoring resource initialization."""

    def test_initialization(self):
        """Test DmarcMonitoring resource initializes correctly."""
        mock_client = Mock()
        resource = DmarcMonitoring(mock_client)

        assert resource.client is mock_client
        assert resource.logger is not None


class TestListMonitors:
    """Test list_monitors method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = DmarcMonitoring(self.mock_client)
        self.resource.logger = Mock()
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_list_monitors_returns_api_response(self):
        """Test list_monitors returns APIResponse."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        result = self.resource.list_monitors()

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_list_monitors_default_params(self):
        """Test list_monitors with no request uses defaults."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        self.resource.list_monitors()

        self.mock_client.request.assert_called_once_with(
            method="GET", path="dmarc-monitoring", params={"page": 1, "limit": 25}
        )

    def test_list_monitors_with_custom_params(self):
        """Test list_monitors with custom pagination."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        query_params = DmarcMonitoringListQueryParams(page=2, limit=50)
        request = DmarcMonitoringListRequest(query_params=query_params)

        self.resource.list_monitors(request)

        self.mock_client.request.assert_called_once_with(
            method="GET", path="dmarc-monitoring", params={"page": 2, "limit": 50}
        )

    def test_list_monitors_with_explicit_request(self):
        """Test list_monitors with explicit request object."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        query_params = DmarcMonitoringListQueryParams(page=1, limit=10)
        request = DmarcMonitoringListRequest(query_params=query_params)

        self.resource.list_monitors(request)

        self.mock_client.request.assert_called_once_with(
            method="GET", path="dmarc-monitoring", params={"page": 1, "limit": 10}
        )


class TestCreateMonitor:
    """Test create_monitor method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = DmarcMonitoring(self.mock_client)
        self.resource.logger = Mock()
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_create_monitor_returns_api_response(self):
        """Test create_monitor returns APIResponse."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringCreateRequest(domain_id="domain-123")
        result = self.resource.create_monitor(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_create_monitor_sends_correct_body(self):
        """Test create_monitor sends domain_id in request body."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringCreateRequest(domain_id="domain-123")
        self.resource.create_monitor(request)

        self.mock_client.request.assert_called_once_with(
            method="POST",
            path="dmarc-monitoring",
            body={"domain_id": "domain-123"},
        )

    def test_create_monitor_uses_post_method(self):
        """Test create_monitor uses POST HTTP method."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringCreateRequest(domain_id="domain-abc")
        self.resource.create_monitor(request)

        call_args = self.mock_client.request.call_args
        assert call_args[1]["method"] == "POST"


class TestUpdateMonitor:
    """Test update_monitor method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = DmarcMonitoring(self.mock_client)
        self.resource.logger = Mock()
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_update_monitor_returns_api_response(self):
        """Test update_monitor returns APIResponse."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringUpdateRequest(
            monitor_id="monitor-123",
            wanted_dmarc_record="v=DMARC1; p=reject;",
        )
        result = self.resource.update_monitor(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_update_monitor_sends_correct_body_and_path(self):
        """Test update_monitor sends wanted_dmarc_record in body and monitor_id in path."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringUpdateRequest(
            monitor_id="monitor-123",
            wanted_dmarc_record="v=DMARC1; p=reject;",
        )
        self.resource.update_monitor(request)

        self.mock_client.request.assert_called_once_with(
            method="PUT",
            path="dmarc-monitoring/monitor-123",
            body={"wanted_dmarc_record": "v=DMARC1; p=reject;"},
        )

    def test_update_monitor_excludes_monitor_id_from_body(self):
        """Test update_monitor does not include monitor_id in request body."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringUpdateRequest(
            monitor_id="monitor-123",
            wanted_dmarc_record="v=DMARC1; p=none;",
        )
        self.resource.update_monitor(request)

        call_args = self.mock_client.request.call_args
        body = call_args[1]["body"]
        assert "monitor_id" not in body
        assert "wanted_dmarc_record" in body


class TestDeleteMonitor:
    """Test delete_monitor method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = DmarcMonitoring(self.mock_client)
        self.resource.logger = Mock()
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_delete_monitor_returns_api_response(self):
        """Test delete_monitor returns APIResponse."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringDeleteRequest(monitor_id="monitor-123")
        result = self.resource.delete_monitor(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_delete_monitor_uses_correct_path(self):
        """Test delete_monitor constructs correct endpoint path."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringDeleteRequest(monitor_id="monitor-abc")
        self.resource.delete_monitor(request)

        self.mock_client.request.assert_called_once_with(
            method="DELETE", path="dmarc-monitoring/monitor-abc"
        )


class TestGetAggregatedReport:
    """Test get_aggregated_report method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = DmarcMonitoring(self.mock_client)
        self.resource.logger = Mock()
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_get_aggregated_report_returns_api_response(self):
        """Test get_aggregated_report returns APIResponse."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringReportRequest(monitor_id="monitor-123")
        result = self.resource.get_aggregated_report(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_get_aggregated_report_default_params(self):
        """Test get_aggregated_report with default pagination."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringReportRequest(monitor_id="monitor-123")
        self.resource.get_aggregated_report(request)

        self.mock_client.request.assert_called_once_with(
            method="GET",
            path="dmarc-monitoring/monitor-123/report",
            params={"page": 1, "limit": 25},
        )

    def test_get_aggregated_report_custom_params(self):
        """Test get_aggregated_report with custom pagination."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        query_params = DmarcMonitoringReportQueryParams(page=3, limit=100)
        request = DmarcMonitoringReportRequest(
            monitor_id="monitor-123", query_params=query_params
        )
        self.resource.get_aggregated_report(request)

        self.mock_client.request.assert_called_once_with(
            method="GET",
            path="dmarc-monitoring/monitor-123/report",
            params={"page": 3, "limit": 100},
        )


class TestGetIpReport:
    """Test get_ip_report method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = DmarcMonitoring(self.mock_client)
        self.resource.logger = Mock()
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_get_ip_report_returns_api_response(self):
        """Test get_ip_report returns APIResponse."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringIpReportRequest(
            monitor_id="monitor-123", ip="192.168.1.1"
        )
        result = self.resource.get_ip_report(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_get_ip_report_constructs_correct_path(self):
        """Test get_ip_report constructs correct endpoint path."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringIpReportRequest(
            monitor_id="monitor-123", ip="10.0.0.1"
        )
        self.resource.get_ip_report(request)

        self.mock_client.request.assert_called_once_with(
            method="GET",
            path="dmarc-monitoring/monitor-123/report/10.0.0.1",
            params={"page": 1, "limit": 25},
        )

    def test_get_ip_report_with_custom_params(self):
        """Test get_ip_report with custom pagination."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        query_params = DmarcMonitoringReportQueryParams(page=2, limit=50)
        request = DmarcMonitoringIpReportRequest(
            monitor_id="monitor-123", ip="10.0.0.1", query_params=query_params
        )
        self.resource.get_ip_report(request)

        self.mock_client.request.assert_called_once_with(
            method="GET",
            path="dmarc-monitoring/monitor-123/report/10.0.0.1",
            params={"page": 2, "limit": 50},
        )


class TestGetReportSources:
    """Test get_report_sources method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = DmarcMonitoring(self.mock_client)
        self.resource.logger = Mock()
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_get_report_sources_returns_api_response(self):
        """Test get_report_sources returns APIResponse."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringReportSourcesRequest(monitor_id="monitor-123")
        result = self.resource.get_report_sources(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_get_report_sources_constructs_correct_path(self):
        """Test get_report_sources constructs correct endpoint path."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringReportSourcesRequest(monitor_id="monitor-abc")
        self.resource.get_report_sources(request)

        self.mock_client.request.assert_called_once_with(
            method="GET",
            path="dmarc-monitoring/monitor-abc/report-sources",
        )


class TestMarkIpFavorite:
    """Test mark_ip_favorite method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = DmarcMonitoring(self.mock_client)
        self.resource.logger = Mock()
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_mark_ip_favorite_returns_api_response(self):
        """Test mark_ip_favorite returns APIResponse."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringFavoriteRequest(
            monitor_id="monitor-123", ip="192.168.1.1"
        )
        result = self.resource.mark_ip_favorite(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_mark_ip_favorite_constructs_correct_path(self):
        """Test mark_ip_favorite constructs correct endpoint path."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringFavoriteRequest(
            monitor_id="monitor-123", ip="10.0.0.1"
        )
        self.resource.mark_ip_favorite(request)

        self.mock_client.request.assert_called_once_with(
            method="PUT",
            path="dmarc-monitoring/monitor-123/favorite/10.0.0.1",
        )


class TestRemoveIpFavorite:
    """Test remove_ip_favorite method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.resource = DmarcMonitoring(self.mock_client)
        self.resource.logger = Mock()
        self.mock_api_response = MagicMock(spec=APIResponse)
        self.resource._create_response = Mock(return_value=self.mock_api_response)

    def test_remove_ip_favorite_returns_api_response(self):
        """Test remove_ip_favorite returns APIResponse."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringFavoriteRequest(
            monitor_id="monitor-123", ip="192.168.1.1"
        )
        result = self.resource.remove_ip_favorite(request)

        assert result == self.mock_api_response
        self.resource._create_response.assert_called_once_with(mock_response)

    def test_remove_ip_favorite_constructs_correct_path(self):
        """Test remove_ip_favorite constructs correct endpoint path."""
        mock_response = Mock()
        self.mock_client.request.return_value = mock_response

        request = DmarcMonitoringFavoriteRequest(
            monitor_id="monitor-123", ip="10.0.0.1"
        )
        self.resource.remove_ip_favorite(request)

        self.mock_client.request.assert_called_once_with(
            method="DELETE",
            path="dmarc-monitoring/monitor-123/favorite/10.0.0.1",
        )


class TestModelValidation:
    """Test model validation."""

    def test_create_request_requires_domain_id(self):
        """Test DmarcMonitoringCreateRequest raises error for empty domain_id."""
        with pytest.raises(Exception):
            DmarcMonitoringCreateRequest(domain_id="")

    def test_update_request_requires_monitor_id(self):
        """Test DmarcMonitoringUpdateRequest raises error for empty monitor_id."""
        with pytest.raises(Exception):
            DmarcMonitoringUpdateRequest(
                monitor_id="", wanted_dmarc_record="v=DMARC1; p=reject;"
            )

    def test_update_request_requires_wanted_dmarc_record(self):
        """Test DmarcMonitoringUpdateRequest raises error for empty wanted_dmarc_record."""
        with pytest.raises(Exception):
            DmarcMonitoringUpdateRequest(monitor_id="monitor-123", wanted_dmarc_record="")

    def test_list_query_params_default_values(self):
        """Test DmarcMonitoringListQueryParams has correct defaults."""
        params = DmarcMonitoringListQueryParams()
        assert params.page == 1
        assert params.limit == 25

    def test_list_query_params_limit_validation(self):
        """Test DmarcMonitoringListQueryParams validates limit range."""
        with pytest.raises(Exception):
            DmarcMonitoringListQueryParams(limit=5)  # below min of 10

        with pytest.raises(Exception):
            DmarcMonitoringListQueryParams(limit=101)  # above max of 100

    def test_favorite_request_requires_ip(self):
        """Test DmarcMonitoringFavoriteRequest raises error for empty ip."""
        with pytest.raises(Exception):
            DmarcMonitoringFavoriteRequest(monitor_id="monitor-123", ip="")

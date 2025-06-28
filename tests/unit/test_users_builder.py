"""Tests for Users API builder."""

import pytest

from mailersend.builders.users import UsersBuilder
from mailersend.models.users import (
    UsersListRequest, UserGetRequest, UserInviteRequest, UserUpdateRequest,
    UserDeleteRequest, InvitesListRequest, InviteGetRequest,
    InviteResendRequest, InviteCancelRequest
)


class TestUsersBuilder:
    """Test UsersBuilder class."""

    def test_builder_initialization(self):
        """Test builder initialization."""
        builder = UsersBuilder()
        assert builder._user_id is None
        assert builder._invite_id is None
        assert builder._email is None
        assert builder._role is None
        assert builder._permissions == []
        assert builder._templates == []
        assert builder._domains == []
        assert builder._requires_periodic_password_change is None

    def test_user_id_method(self):
        """Test user_id method."""
        builder = UsersBuilder()
        result = builder.user_id("user123")
        assert result is builder  # method chaining
        assert builder._user_id == "user123"

    def test_invite_id_method(self):
        """Test invite_id method."""
        builder = UsersBuilder()
        result = builder.invite_id("invite123")
        assert result is builder  # method chaining
        assert builder._invite_id == "invite123"

    def test_email_method(self):
        """Test email method."""
        builder = UsersBuilder()
        result = builder.email("user@example.com")
        assert result is builder  # method chaining
        assert builder._email == "user@example.com"

    def test_role_method(self):
        """Test role method."""
        builder = UsersBuilder()
        result = builder.role("Admin")
        assert result is builder  # method chaining
        assert builder._role == "Admin"

    def test_permissions_method(self):
        """Test permissions method."""
        builder = UsersBuilder()
        permissions = ["read-templates", "manage-domain"]
        result = builder.permissions(permissions)
        assert result is builder  # method chaining
        assert builder._permissions == permissions
        assert builder._permissions is not permissions  # should be a copy

    def test_add_permission_method(self):
        """Test add_permission method."""
        builder = UsersBuilder()
        result = builder.add_permission("read-templates")
        assert result is builder  # method chaining
        assert "read-templates" in builder._permissions
        
        # Test adding duplicate permission
        builder.add_permission("read-templates")
        assert builder._permissions.count("read-templates") == 1

    def test_templates_method(self):
        """Test templates method."""
        builder = UsersBuilder()
        templates = ["template1", "template2"]
        result = builder.templates(templates)
        assert result is builder  # method chaining
        assert builder._templates == templates
        assert builder._templates is not templates  # should be a copy

    def test_add_template_method(self):
        """Test add_template method."""
        builder = UsersBuilder()
        result = builder.add_template("template1")
        assert result is builder  # method chaining
        assert "template1" in builder._templates
        
        # Test adding duplicate template
        builder.add_template("template1")
        assert builder._templates.count("template1") == 1

    def test_domains_method(self):
        """Test domains method."""
        builder = UsersBuilder()
        domains = ["domain1", "domain2"]
        result = builder.domains(domains)
        assert result is builder  # method chaining
        assert builder._domains == domains
        assert builder._domains is not domains  # should be a copy

    def test_add_domain_method(self):
        """Test add_domain method."""
        builder = UsersBuilder()
        result = builder.add_domain("domain1")
        assert result is builder  # method chaining
        assert "domain1" in builder._domains
        
        # Test adding duplicate domain
        builder.add_domain("domain1")
        assert builder._domains.count("domain1") == 1

    def test_requires_periodic_password_change_method(self):
        """Test requires_periodic_password_change method."""
        builder = UsersBuilder()
        result = builder.requires_periodic_password_change(True)
        assert result is builder  # method chaining
        assert builder._requires_periodic_password_change is True

    def test_role_helper_methods(self):
        """Test role helper methods."""
        builder = UsersBuilder()
        
        # Test admin_role
        result = builder.admin_role()
        assert result is builder
        assert builder._role == "Admin"
        
        # Test manager_role
        builder.reset().manager_role()
        assert builder._role == "Manager"
        
        # Test designer_role
        builder.reset().designer_role()
        assert builder._role == "Designer"
        
        # Test accountant_role
        builder.reset().accountant_role()
        assert builder._role == "Accountant"
        
        # Test custom_user_role
        builder.reset().custom_user_role()
        assert builder._role == "Custom User"

    def test_permission_helper_methods(self):
        """Test permission helper methods."""
        builder = UsersBuilder()
        
        # Test template_permissions
        result = builder.template_permissions()
        assert result is builder
        assert "read-all-templates" in builder._permissions
        assert "read-own-templates" in builder._permissions
        assert "manage-template" in builder._permissions
        assert "read-filemanager" in builder._permissions
        
        # Test domain_permissions
        builder.reset().domain_permissions()
        assert "manage-domain" in builder._permissions
        assert "manage-inbound" in builder._permissions
        assert "manage-webhook" in builder._permissions
        assert "control-sendings" in builder._permissions
        
        # Test analytics_permissions
        builder.reset().analytics_permissions()
        assert "read-recipient" in builder._permissions
        assert "read-activity" in builder._permissions
        assert "read-email" in builder._permissions
        assert "read-analytics" in builder._permissions
        
        # Test account_permissions
        builder.reset().account_permissions()
        assert "manage-account" in builder._permissions
        assert "read-invoice" in builder._permissions
        assert "manage-api-token" in builder._permissions
        assert "read-suppressions" in builder._permissions

    def test_permission_helpers_no_duplicates(self):
        """Test permission helpers don't add duplicates."""
        builder = UsersBuilder()
        builder.add_permission("read-templates")
        builder.template_permissions()
        # Should not have duplicates even if permission already exists
        assert builder._permissions.count("read-templates") <= 1

    def test_reset_method(self):
        """Test reset method."""
        builder = UsersBuilder()
        builder.user_id("user123").email("user@example.com").role("Admin")
        builder.permissions(["read-templates"]).templates(["template1"])
        builder.requires_periodic_password_change(True)
        
        result = builder.reset()
        assert result is builder  # method chaining
        assert builder._user_id is None
        assert builder._email is None
        assert builder._role is None
        assert builder._permissions == []
        assert builder._templates == []
        assert builder._domains == []
        assert builder._requires_periodic_password_change is None

    def test_copy_method(self):
        """Test copy method."""
        builder = UsersBuilder()
        builder.user_id("user123").email("user@example.com").role("Admin")
        builder.permissions(["read-templates"]).templates(["template1"])
        builder.domains(["domain1"]).requires_periodic_password_change(True)
        
        copied = builder.copy()
        assert copied is not builder
        assert copied._user_id == builder._user_id
        assert copied._email == builder._email
        assert copied._role == builder._role
        assert copied._permissions == builder._permissions
        assert copied._permissions is not builder._permissions  # different list
        assert copied._templates == builder._templates
        assert copied._templates is not builder._templates  # different list
        assert copied._domains == builder._domains
        assert copied._domains is not builder._domains  # different list
        assert copied._requires_periodic_password_change == builder._requires_periodic_password_change

    def test_method_chaining(self):
        """Test method chaining works correctly."""
        builder = UsersBuilder()
        result = (builder
                  .user_id("user123")
                  .email("user@example.com")
                  .role("Custom User")
                  .add_permission("read-templates")
                  .add_template("template1")
                  .add_domain("domain1")
                  .requires_periodic_password_change(True))
        
        assert result is builder
        assert builder._user_id == "user123"
        assert builder._email == "user@example.com"
        assert builder._role == "Custom User"
        assert "read-templates" in builder._permissions
        assert "template1" in builder._templates
        assert "domain1" in builder._domains
        assert builder._requires_periodic_password_change is True


class TestUsersBuilderBuildMethods:
    """Test UsersBuilder build methods."""

    def test_build_users_list(self):
        """Test build_users_list method."""
        builder = UsersBuilder()
        request = builder.build_users_list()
        assert isinstance(request, UsersListRequest)

    def test_build_user_get_success(self):
        """Test build_user_get method with valid data."""
        builder = UsersBuilder()
        request = builder.user_id("user123").build_user_get()
        assert isinstance(request, UserGetRequest)
        assert request.user_id == "user123"

    def test_build_user_get_missing_user_id(self):
        """Test build_user_get method without user_id."""
        builder = UsersBuilder()
        with pytest.raises(ValueError, match="user_id is required for getting a user"):
            builder.build_user_get()

    def test_build_user_invite_success(self):
        """Test build_user_invite method with valid data."""
        builder = UsersBuilder()
        request = (builder
                   .email("user@example.com")
                   .role("Admin")
                   .permissions(["read-templates"])
                   .templates(["template1"])
                   .domains(["domain1"])
                   .requires_periodic_password_change(True)
                   .build_user_invite())
        
        assert isinstance(request, UserInviteRequest)
        assert request.email == "user@example.com"
        assert request.role == "Admin"
        assert request.permissions == ["read-templates"]
        assert request.templates == ["template1"]
        assert request.domains == ["domain1"]
        assert request.requires_periodic_password_change is True

    def test_build_user_invite_missing_email(self):
        """Test build_user_invite method without email."""
        builder = UsersBuilder()
        with pytest.raises(ValueError, match="email is required for inviting a user"):
            builder.role("Admin").build_user_invite()

    def test_build_user_invite_missing_role(self):
        """Test build_user_invite method without role."""
        builder = UsersBuilder()
        with pytest.raises(ValueError, match="role is required for inviting a user"):
            builder.email("user@example.com").build_user_invite()

    def test_build_user_update_success(self):
        """Test build_user_update method with valid data."""
        builder = UsersBuilder()
        request = (builder
                   .user_id("user123")
                   .role("Manager")
                   .permissions(["read-templates"])
                   .templates(["template1"])
                   .domains(["domain1"])
                   .requires_periodic_password_change(False)
                   .build_user_update())
        
        assert isinstance(request, UserUpdateRequest)
        assert request.user_id == "user123"
        assert request.role == "Manager"
        assert request.permissions == ["read-templates"]
        assert request.templates == ["template1"]
        assert request.domains == ["domain1"]
        assert request.requires_periodic_password_change is False

    def test_build_user_update_missing_user_id(self):
        """Test build_user_update method without user_id."""
        builder = UsersBuilder()
        with pytest.raises(ValueError, match="user_id is required for updating a user"):
            builder.role("Manager").build_user_update()

    def test_build_user_update_missing_role(self):
        """Test build_user_update method without role."""
        builder = UsersBuilder()
        with pytest.raises(ValueError, match="role is required for updating a user"):
            builder.user_id("user123").build_user_update()

    def test_build_user_delete_success(self):
        """Test build_user_delete method with valid data."""
        builder = UsersBuilder()
        request = builder.user_id("user123").build_user_delete()
        assert isinstance(request, UserDeleteRequest)
        assert request.user_id == "user123"

    def test_build_user_delete_missing_user_id(self):
        """Test build_user_delete method without user_id."""
        builder = UsersBuilder()
        with pytest.raises(ValueError, match="user_id is required for deleting a user"):
            builder.build_user_delete()

    def test_build_invites_list(self):
        """Test build_invites_list method."""
        builder = UsersBuilder()
        request = builder.build_invites_list()
        assert isinstance(request, InvitesListRequest)

    def test_build_invite_get_success(self):
        """Test build_invite_get method with valid data."""
        builder = UsersBuilder()
        request = builder.invite_id("invite123").build_invite_get()
        assert isinstance(request, InviteGetRequest)
        assert request.invite_id == "invite123"

    def test_build_invite_get_missing_invite_id(self):
        """Test build_invite_get method without invite_id."""
        builder = UsersBuilder()
        with pytest.raises(ValueError, match="invite_id is required for getting an invite"):
            builder.build_invite_get()

    def test_build_invite_resend_success(self):
        """Test build_invite_resend method with valid data."""
        builder = UsersBuilder()
        request = builder.invite_id("invite123").build_invite_resend()
        assert isinstance(request, InviteResendRequest)
        assert request.invite_id == "invite123"

    def test_build_invite_resend_missing_invite_id(self):
        """Test build_invite_resend method without invite_id."""
        builder = UsersBuilder()
        with pytest.raises(ValueError, match="invite_id is required for resending an invite"):
            builder.build_invite_resend()

    def test_build_invite_cancel_success(self):
        """Test build_invite_cancel method with valid data."""
        builder = UsersBuilder()
        request = builder.invite_id("invite123").build_invite_cancel()
        assert isinstance(request, InviteCancelRequest)
        assert request.invite_id == "invite123"

    def test_build_invite_cancel_missing_invite_id(self):
        """Test build_invite_cancel method without invite_id."""
        builder = UsersBuilder()
        with pytest.raises(ValueError, match="invite_id is required for canceling an invite"):
            builder.build_invite_cancel()


class TestUsersBuilderComplexScenarios:
    """Test complex scenarios with UsersBuilder."""

    def test_builder_reuse_after_reset(self):
        """Test builder can be reused after reset."""
        builder = UsersBuilder()
        
        # First use
        request1 = (builder
                    .user_id("user1")
                    .email("user1@example.com")
                    .role("Admin")
                    .build_user_invite())
        assert request1.email == "user1@example.com"
        
        # Reset and reuse
        request2 = (builder
                    .reset()
                    .user_id("user2")
                    .email("user2@example.com")
                    .role("Manager")
                    .build_user_invite())
        assert request2.email == "user2@example.com"
        assert request2.role == "Manager"

    def test_builder_copy_independence(self):
        """Test copied builder is independent."""
        builder1 = UsersBuilder()
        builder1.user_id("user1").email("user1@example.com").role("Admin")
        
        builder2 = builder1.copy()
        builder2.user_id("user2").email("user2@example.com").role("Manager")
        
        # Original should be unchanged
        assert builder1._user_id == "user1"
        assert builder1._email == "user1@example.com"
        assert builder1._role == "Admin"
        
        # Copy should have new values
        assert builder2._user_id == "user2"
        assert builder2._email == "user2@example.com"
        assert builder2._role == "Manager"

    def test_permission_helpers_combinations(self):
        """Test combining multiple permission helpers."""
        builder = UsersBuilder()
        builder.template_permissions().domain_permissions().analytics_permissions()
        
        # Should have permissions from all categories
        assert "read-all-templates" in builder._permissions  # from template_permissions
        assert "manage-domain" in builder._permissions  # from domain_permissions
        assert "read-analytics" in builder._permissions  # from analytics_permissions
        
        # Should not have duplicates
        all_permissions = builder._permissions
        assert len(all_permissions) == len(set(all_permissions))

    def test_build_methods_maintain_state(self):
        """Test build methods don't modify builder state."""
        builder = UsersBuilder()
        builder.user_id("user123").email("user@example.com").role("Admin")
        
        # Build request
        request = builder.build_user_invite()
        
        # State should be preserved
        assert builder._user_id == "user123"
        assert builder._email == "user@example.com"
        assert builder._role == "Admin"
        
        # Can build again with same state
        request2 = builder.build_user_invite()
        assert request2.email == request.email
        assert request2.role == request.role 
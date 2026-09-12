"""
Unit tests for CloudInfraSetupAgent.
"""
import unittest
from unittest.mock import Mock, patch
from agents.cloud_infra_agent import CloudInfraSetupAgent
from agents.config import AgentConfig


class TestCloudInfraSetupAgent(unittest.TestCase):
    """Test cases for CloudInfraSetupAgent"""

    def setUp(self):
        """Set up agent with empty config for testing"""
        self.config = AgentConfig(
            openai_api_key="",
            zoom_client_id="",
            zoom_client_secret="",
            zoom_account_id="",
            usertesting_api_key="",
            notion_api_key="",
            notion_database_id="",
            github_token=""
        )
        self.agent = CloudInfraSetupAgent(self.config)

    def test_agent_initialization(self):
        """Test that agent initializes correctly"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(len(self.agent.execution_log), 0)

    def test_parse_inputs_valid_aws(self):
        """Test input parsing with valid AWS provider"""
        reqs = {
            "compute": {"instance_type": "t3.medium"},
            "storage": {"bucket_name": "my-aws-bucket"}
        }
        guidelines = {
            "iam": {"roles": ["admin"]}
        }
        parsed = self.agent._parse_inputs("aws", reqs, guidelines)
        self.assertEqual(parsed["provider"], "AWS")
        self.assertEqual(parsed["requirements"]["compute"]["instance_type"], "t3.medium")
        self.assertEqual(parsed["guidelines"]["iam"]["roles"], ["admin"])

    def test_parse_inputs_valid_gcp(self):
        """Test input parsing with valid GCP provider"""
        parsed = self.agent._parse_inputs("gcp", {}, {})
        self.assertEqual(parsed["provider"], "GCP")
        # Should populate defaults when requirements/guidelines are empty
        self.assertIn("compute", parsed["requirements"])
        self.assertIn("iam", parsed["guidelines"])

    def test_parse_inputs_valid_azure(self):
        """Test input parsing with valid Azure provider"""
        parsed = self.agent._parse_inputs("Azure", {}, {})
        self.assertEqual(parsed["provider"], "AZURE")

    def test_parse_inputs_invalid_provider(self):
        """Test input parsing raises ValueError with unsupported provider"""
        with self.assertRaises(ValueError):
            self.agent._parse_inputs("OracleCloud", {}, {})

    def test_generate_terraform_files_aws(self):
        """Test Terraform file generation for AWS"""
        reqs = {
            "compute": {"instance_type": "t3.large"},
            "storage": {"bucket_name": "custom-s3-bucket-name"},
            "networking": {"vpc_cidr": "172.16.0.0/16"},
            "database": {"instance_class": "db.t3.medium", "db_type": "postgres"}
        }
        files = self.agent._generate_terraform_files("AWS", reqs, {})
        self.assertIn("main.tf", files)
        self.assertIn("variables.tf", files)
        self.assertIn("outputs.tf", files)

        self.assertIn("172.16.0.0/16", files["variables.tf"])
        self.assertIn("t3.large", files["variables.tf"])
        self.assertIn("custom-s3-bucket-name", files["variables.tf"])
        self.assertIn("db.t3.medium", files["variables.tf"])

        self.assertIn("resource \"aws_vpc\" \"main\"", files["main.tf"])
        self.assertIn("resource \"aws_s3_bucket\" \"storage\"", files["main.tf"])
        self.assertIn("resource \"random_password\" \"db_password\"", files["main.tf"])

    def test_generate_terraform_files_gcp(self):
        """Test Terraform file generation for GCP"""
        reqs = {
            "compute": {"instance_type": "n2-standard-2"},
            "storage": {"bucket_name": "custom-gcp-bucket"},
            "networking": {"vpc_cidr": "10.10.0.0/16"},
            "database": {"instance_class": "db-custom-tier"}
        }
        files = self.agent._generate_terraform_files("GCP", reqs, {})
        self.assertIn("main.tf", files)
        self.assertIn("variables.tf", files)
        self.assertIn("outputs.tf", files)

        self.assertIn("10.10.0.0/16", files["variables.tf"])
        self.assertIn("n2-standard-2", files["variables.tf"])
        self.assertIn("custom-gcp-bucket", files["variables.tf"])
        self.assertIn("db-custom-tier", files["variables.tf"])

        self.assertIn("resource \"google_compute_network\" \"main\"", files["main.tf"])
        self.assertIn("resource \"google_storage_bucket\" \"storage\"", files["main.tf"])

    def test_generate_terraform_files_azure(self):
        """Test Terraform file generation for Azure"""
        reqs = {
            "compute": {"instance_type": "Standard_D2s_v3"},
            "storage": {"bucket_name": "customazurestorage"},
            "networking": {"vpc_cidr": "10.20.0.0/16"},
            "database": {"instance_class": "GP_Gen5_2"}
        }
        files = self.agent._generate_terraform_files("AZURE", reqs, {})
        self.assertIn("main.tf", files)
        self.assertIn("variables.tf", files)
        self.assertIn("outputs.tf", files)

        self.assertIn("10.20.0.0/16", files["variables.tf"])
        self.assertIn("Standard_D2s_v3", files["variables.tf"])
        self.assertIn("customazurestorage", files["variables.tf"])
        self.assertIn("GP_Gen5_2", files["variables.tf"])

        self.assertIn("resource \"azurerm_virtual_network\" \"main\"", files["main.tf"])
        self.assertIn("resource \"azurerm_storage_account\" \"storage\"", files["main.tf"])
        self.assertIn("resource \"random_password\" \"db_password\"", files["main.tf"])

    def test_full_workflow_execution_success_aws(self):
        """Test full successful execute workflow with AWS in simulation mode"""
        results = self.agent.execute(
            cloud_provider_preference="AWS",
            infrastructure_requirements={},
            security_policy_guidelines={},
            simulate=True
        )

        self.assertEqual(results["status"], "success")
        self.assertIn("TerraformPlanOutput", results)
        self.assertIn("TerraformApplyLog", results)
        self.assertIn("CloudResourceStatusReport", results)
        self.assertIn("github_issue_url", results)
        self.assertIn("execution_log", results)

        # Execution log should have 18 entries (9 steps * 2 (start/complete))
        self.assertEqual(len(results["execution_log"]), 18)

        # Verify step order in execution log
        for i in range(1, 10):
            step_entries = [entry for entry in results["execution_log"] if entry["step"] == i]
            self.assertEqual(len(step_entries), 2)
            self.assertEqual(step_entries[0]["status"], "started")
            self.assertEqual(step_entries[1]["status"], "completed")

        self.assertIn("aws_vpc.main will be created", results["TerraformPlanOutput"])
        self.assertIn("aws_db_instance.database: Creation complete", results["TerraformApplyLog"])
        self.assertIn("VPC", results["CloudResourceStatusReport"])
        self.assertIn("EC2 Instance", results["CloudResourceStatusReport"])
        self.assertIn("RDS Database", results["CloudResourceStatusReport"])

    def test_full_workflow_execution_success_gcp(self):
        """Test full successful execute workflow with GCP"""
        results = self.agent.execute(
            cloud_provider_preference="GCP",
            infrastructure_requirements={},
            security_policy_guidelines={},
            simulate=True
        )

        self.assertEqual(results["status"], "success")
        self.assertIn("google_compute_instance.web will be created", results["TerraformPlanOutput"])
        self.assertIn("google_sql_database_instance.database: Creation complete", results["TerraformApplyLog"])
        self.assertIn("GCS Bucket", results["CloudResourceStatusReport"])

    def test_full_workflow_execution_success_azure(self):
        """Test full successful execute workflow with Azure"""
        results = self.agent.execute(
            cloud_provider_preference="AZURE",
            infrastructure_requirements={},
            security_policy_guidelines={},
            simulate=True
        )

        self.assertEqual(results["status"], "success")
        self.assertIn("azurerm_linux_virtual_machine.web will be created", results["TerraformPlanOutput"])
        self.assertIn("azurerm_mssql_database.db: Creation complete", results["TerraformApplyLog"])
        self.assertIn("Storage Account", results["CloudResourceStatusReport"])

    def test_execute_handles_exceptions_gracefully(self):
        """Test execution handles exceptions in early stage and returns structured error response"""
        # Trigger an exception by passing an invalid provider
        results = self.agent.execute(
            cloud_provider_preference="InvalidProvider",
            infrastructure_requirements={},
            security_policy_guidelines={},
            simulate=True
        )

        self.assertEqual(results["status"], "error")
        self.assertIn("error", results)
        self.assertIn("Unsupported cloud provider", results["error"])
        self.assertEqual(results["TerraformPlanOutput"], "")
        self.assertEqual(results["TerraformApplyLog"], "")
        self.assertEqual(results["CloudResourceStatusReport"], "")
        self.assertIsNone(results["github_issue_url"])
        self.assertEqual(len(results["execution_log"]), 2)  # Step 1 started and failed
        self.assertEqual(results["execution_log"][1]["status"], "failed")

    @patch("agents.cloud_infra_agent.requests.post")
    def test_github_issue_creation_with_real_token(self, mock_post):
        """Test that GitHub API is called when a real token is provided"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"html_url": "https://github.com/myorg/myrepo/issues/42"}
        mock_post.return_value = mock_response

        # Set up agent with config having a real-looking token
        config = AgentConfig(
            github_token="ghp_realtoken1234567890",
            github_repo="myorg/myrepo"
        )
        agent = CloudInfraSetupAgent(config)

        results = agent.execute(
            cloud_provider_preference="AWS",
            infrastructure_requirements={},
            security_policy_guidelines={},
            simulate=True
        )

        self.assertEqual(results["status"], "success")
        self.assertEqual(results["github_issue_url"], "https://github.com/myorg/myrepo/issues/42")
        mock_post.assert_called_once()

    @patch("agents.cloud_infra_agent.shutil.which")
    @patch("agents.cloud_infra_agent.subprocess.run")
    def test_real_execution_with_all_binaries_present(self, mock_run, mock_which):
        """Test real non-simulated execution path when all required CLI binaries exist on PATH"""
        # Mock that terraform and cloud CLIs exist
        mock_which.return_value = "/usr/local/bin/dummy"

        # Mock successful subprocess outputs
        mock_init = Mock(returncode=0, stdout="Terraform initialized successfully!", stderr="")
        mock_validate = Mock(returncode=0, stdout="Configuration validated successfully!", stderr="")
        mock_plan = Mock(returncode=0, stdout="Plan: 7 to add, 0 to change, 0 to destroy.", stderr="")
        mock_apply = Mock(returncode=0, stdout="Apply complete! Resources: 7 added.", stderr="")
        mock_cli = Mock(returncode=0, stdout='{"Vpcs": [{"VpcId": "vpc-0d48f22bb48f657a1"}]}', stderr="")

        mock_run.side_effect = [mock_init, mock_validate, mock_plan, mock_apply, mock_cli]

        results = self.agent.execute(
            cloud_provider_preference="AWS",
            infrastructure_requirements={},
            security_policy_guidelines={},
            simulate=False
        )

        self.assertEqual(results["status"], "success")
        self.assertIn("Plan: 7 to add, 0 to change, 0 to destroy.", results["TerraformPlanOutput"])
        self.assertIn("Apply complete! Resources: 7 added.", results["TerraformApplyLog"])
        self.assertIn("VPC", results["CloudResourceStatusReport"])

        # Check mock run is called with correct commands
        self.assertEqual(mock_run.call_count, 5)
        # First call: terraform init
        self.assertEqual(mock_run.call_args_list[0][0][0], ["terraform", "init"])
        # Second call: terraform validate
        self.assertEqual(mock_run.call_args_list[1][0][0], ["terraform", "validate"])
        # Third call: terraform plan
        self.assertEqual(mock_run.call_args_list[2][0][0], ["terraform", "plan", "-no-color"])
        # Fourth call: terraform apply
        self.assertEqual(mock_run.call_args_list[3][0][0], ["terraform", "apply", "-auto-approve", "-no-color"])
        # Fifth call: aws ec2 describe-vpcs
        self.assertEqual(mock_run.call_args_list[4][0][0], ["aws", "ec2", "describe-vpcs", "--filter", "Name=tag:Name,Values=main-vpc"])

    @patch("agents.cloud_infra_agent.shutil.which")
    def test_real_execution_raises_error_when_terraform_is_missing(self, mock_which):
        """Test that real execution fails immediately and reports error when terraform binary is not found on PATH"""
        mock_which.return_value = None  # Mock terraform not found

        results = self.agent.execute(
            cloud_provider_preference="AWS",
            infrastructure_requirements={},
            security_policy_guidelines={},
            simulate=False
        )

        self.assertEqual(results["status"], "error")
        self.assertIn("error", results)
        self.assertIn("Executable 'terraform' not found on system PATH", results["error"])


if __name__ == "__main__":
    unittest.main()

"""Test to verify behavior of directory suffix based type."""
import subprocess

from runway.util import change_dir

from integration_tests.test_runway_module_type_detection.test_runway_module_type_detection import (
    RunwayModuleTypeDetection
)


class TestSuffixTypeCFN(RunwayModuleTypeDetection):
    """Test to verify a 'type' directory suffix 'cfn' is respected."""

    TEST_NAME = __name__

    def deploy(self):
        """Deploy provider."""
        self.copy_fixture('sampleapp.cfn')
        self.copy_runway('suffix-cfn')
        with change_dir(self.mtd_test_dir):
            out = subprocess.check_output(['runway', 'deploy'], stderr=subprocess.STDOUT)
            return 0 if "Skipping stacker build" in out.decode() else -1

    def run(self):
        """Run tests."""
        self.clean()
        assert self.deploy() == 0, '{}:Directory Suffix Type CFN Failed'.format(__name__)

    def teardown(self):
        """Teardown."""
        self.logger.info('Tearing down: %s', self.TEST_NAME)
        self.clean()

import unittest
from unittest.mock import patch, MagicMock
import os
from sagemaker_pytorch_serving_container.serving import configure_log_level

import unittest
from unittest.mock import patch, MagicMock
import os
from your_module import configure_log_level  # replace 'your_module' with the actual module name

class TestLogConfig(unittest.TestCase):

    @patch('os.environ.get')
    @patch('subprocess.run')
    def test_valid_log_level(self, mock_run, mock_env_get):
        mock_env_get.return_value = '20'
        mock_run.return_value = MagicMock(returncode=0)
        
        result = configure_log_level()
        
        self.assertEqual(result, "Logging level set to error")
        mock_run.assert_called_once()

    @patch('os.environ.get')
    def test_invalid_log_level(self, mock_env_get):
        mock_env_get.return_value = '70'
        
        result = configure_log_level()
        
        self.assertEqual(result, "Invalid TS_LOGLEVEL value: 70. No changes made to logging configuration.")

    @patch('os.environ.get')
    def test_no_log_level_set(self, mock_env_get):
        mock_env_get.return_value = None
        
        result = configure_log_level()
        
        self.assertEqual(result, "TS_LOGLEVEL not set. Using default logging configuration.")

    @patch('os.environ.get')
    @patch('subprocess.run')
    def test_subprocess_error(self, mock_run, mock_env_get):
        mock_env_get.return_value = '20'
        mock_run.side_effect = subprocess.CalledProcessError(1, 'sed')
        
        result = configure_log_level()
        
        self.assertTrue(result.startswith("Error configuring the logging"))

if __name__ == '__main__':
    unittest.main()
import pytest
from .quart_motor_tests import TestQuartMotor, TestCollection

if __name__ == '__main__':
    pytest.main(['--color=auto', '--no-cov', '-v'])

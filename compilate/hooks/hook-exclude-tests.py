# Hook to exclude test files from the build
from PyInstaller.utils.hooks import collect_data_files

# Exclude test files
excludedimports = [
    'tests',
    'test_*',
    '*test*',
    'pytest',
    'pytest_mock',
    'httpx'
]

# Exclude data files from tests directory
datas = []
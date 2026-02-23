import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Store the original activities state
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture()
def client():
    """
    Arrange: Reset activities to original state before each test
    Act: Provide a TestClient for HTTP requests
    Assert: Restore original activities after test completes
    """
    # Arrange: Reset activities to clean state
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    
    # Act: Create and yield test client
    test_client = TestClient(app)
    yield test_client
    
    # Assert/Cleanup: Restore original state after test
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))

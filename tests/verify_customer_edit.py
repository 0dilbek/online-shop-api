import sys
import os

# Add project root to sys.path
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from app.main import app

def test_customer_update():
    client = TestClient(app)
    
    # 1. Create a customer
    payload = {
        "full_name": "Test User",
        "phone": "998901234567",
        "password": "password123",
        "default_address": "Initial Address"
    }
    response = client.post("/api/v1/customers", json=payload)
    
    customer_id = None
    if response.status_code == 200:
        customer_id = response.json()["id"]
    elif response.status_code == 400 and "already exists" in response.text:
        # Get existing customer by phone
        response = client.get(f"/api/v1/customers/by-phone?phone={payload['phone']}")
        assert response.status_code == 200
        customer_id = response.json()["id"]
    else:
        print(f"Failed to setup test customer: {response.status_code} {response.text}")
        sys.exit(1)

    # 2. Update the customer
    update_payload = {
        "full_name": "Updated User",
        "default_address": "Updated Address"
    }
    response = client.patch(f"/api/v1/customers/{customer_id}", json=update_payload)
    if response.status_code != 200:
        print(f"PATCH failed: {response.status_code} {response.text}")
        assert response.status_code == 200
        
    data = response.json()
    assert data["full_name"] == "Updated User"
    assert data["default_address"] == "Updated Address"
    assert data["phone"] == payload["phone"] # remains unchanged

    # 3. Verify fetch
    response = client.get(f"/api/v1/customers/{customer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated User"
    
    print("Verification successful!")

if __name__ == "__main__":
    try:
        test_customer_update()
    except Exception as e:
        print(f"Verification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

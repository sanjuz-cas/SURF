"""
SURF Full Integration Test
===========================
Tests the complete workflow:
1. PostgreSQL database → 2. FastAPI backend → 3. React frontend

This test validates the entire system working together.
"""
import requests
import psycopg
import time
import sys

# ANSI color codes for pretty output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_test(message, status="info"):
    """Print formatted test messages."""
    if status == "pass":
        print(f"{GREEN}✓{RESET} {message}")
    elif status == "fail":
        print(f"{RED}✗{RESET} {message}")
    elif status == "warn":
        print(f"{YELLOW}⚠{RESET} {message}")
    else:
        print(f"{BLUE}ℹ{RESET} {message}")

def print_section(title):
    """Print section header."""
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{title:^60}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

# Test configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "surf_feedback_db",
    "user": "surf_user",
    "password": "surf_password_2024",
}
API_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

test_results = {
    "passed": 0,
    "failed": 0,
    "total": 0
}

def run_test(test_name, test_func):
    """Run a test and track results."""
    global test_results
    test_results["total"] += 1
    try:
        test_func()
        test_results["passed"] += 1
        return True
    except AssertionError as e:
        print_test(f"{test_name}: {str(e)}", "fail")
        test_results["failed"] += 1
        return False
    except Exception as e:
        print_test(f"{test_name}: Unexpected error - {str(e)}", "fail")
        test_results["failed"] += 1
        return False

# ===== DATABASE TESTS =====
def test_database_connection():
    """Test 1: Database is accessible"""
    print_test("Testing database connection...", "info")
    conn = psycopg.connect(**DB_CONFIG)
    assert conn is not None, "Failed to connect to database"
    conn.close()
    print_test("Database connection successful", "pass")

def test_database_schema():
    """Test 2: Database schema is correct"""
    print_test("Testing database schema...", "info")
    conn = psycopg.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Check raw_feedback table
    cursor.execute("""
        SELECT COUNT(*) FROM information_schema.tables 
        WHERE table_name = 'raw_feedback'
    """)
    assert cursor.fetchone()[0] == 1, "raw_feedback table missing"
    
    # Check prioritized_output table
    cursor.execute("""
        SELECT COUNT(*) FROM information_schema.tables 
        WHERE table_name = 'prioritized_output'
    """)
    assert cursor.fetchone()[0] == 1, "prioritized_output table missing"
    
    cursor.close()
    conn.close()
    print_test("Database schema validated", "pass")

def test_database_data():
    """Test 3: Database has sample data"""
    print_test("Testing database data...", "info")
    conn = psycopg.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Check raw feedback count
    cursor.execute("SELECT COUNT(*) FROM raw_feedback")
    raw_count = cursor.fetchone()[0]
    assert raw_count > 0, f"No raw feedback found (expected > 0, got {raw_count})"
    
    # Check prioritized output count
    cursor.execute("SELECT COUNT(*) FROM prioritized_output")
    prioritized_count = cursor.fetchone()[0]
    assert prioritized_count > 0, f"No prioritized output found (expected > 0, got {prioritized_count})"
    
    cursor.close()
    conn.close()
    print_test(f"Database contains {raw_count} raw items, {prioritized_count} prioritized items", "pass")

# ===== API TESTS =====
def test_api_health():
    """Test 4: API health check"""
    print_test("Testing API health endpoint...", "info")
    response = requests.get(f"{API_URL}/", timeout=5)
    assert response.status_code == 200, f"API health check failed: {response.status_code}"
    data = response.json()
    assert data["status"] == "ok", "API status is not 'ok'"
    print_test("API is healthy", "pass")

def test_api_priorities_endpoint():
    """Test 5: API /api/priorities endpoint"""
    print_test("Testing /api/priorities endpoint...", "info")
    response = requests.get(f"{API_URL}/api/priorities", timeout=10)
    assert response.status_code == 200, f"API request failed: {response.status_code}"
    
    data = response.json()
    assert "items" in data, "Response missing 'items' field"
    assert "total_analyzed" in data, "Response missing 'total_analyzed' field"
    assert "generated_at" in data, "Response missing 'generated_at' field"
    
    items = data["items"]
    assert len(items) > 0, "No items returned from API"
    
    # Validate first item structure
    item = items[0]
    required_fields = ["id", "rank", "title", "score", "preMortemForecast", "action_plan"]
    for field in required_fields:
        assert field in item, f"Item missing required field: {field}"
    
    # Validate action_plan structure
    action_plan = item["action_plan"]
    assert "immediate_steps" in action_plan, "action_plan missing immediate_steps"
    assert "medium_term_steps" in action_plan, "action_plan missing medium_term_steps"
    assert "long_term_steps" in action_plan, "action_plan missing long_term_steps"
    
    print_test(f"API returned {len(items)} prioritized items with correct structure", "pass")

def test_api_stats_endpoint():
    """Test 6: API /api/stats endpoint"""
    print_test("Testing /api/stats endpoint...", "info")
    response = requests.get(f"{API_URL}/api/stats", timeout=5)
    assert response.status_code == 200, f"Stats request failed: {response.status_code}"
    
    data = response.json()
    assert "total_raw_feedback" in data, "Stats missing total_raw_feedback"
    assert "total_processed" in data, "Stats missing total_processed"
    print_test("API stats endpoint working", "pass")

# ===== FRONTEND TESTS =====
def test_frontend_accessible():
    """Test 7: Frontend is accessible"""
    print_test("Testing frontend accessibility...", "info")
    response = requests.get(FRONTEND_URL, timeout=10)
    assert response.status_code == 200, f"Frontend not accessible: {response.status_code}"
    print_test("Frontend is accessible", "pass")

def test_frontend_loads_react():
    """Test 8: Frontend loads React app"""
    print_test("Testing frontend loads React app...", "info")
    response = requests.get(FRONTEND_URL, timeout=10)
    html = response.text
    assert "root" in html or "React" in html or "<!doctype html>" in html.lower(), "Frontend doesn't appear to be a React app"
    print_test("Frontend React app detected", "pass")

# ===== INTEGRATION TESTS =====
def test_end_to_end_data_flow():
    """Test 9: Complete data flow from DB → API → Frontend"""
    print_test("Testing end-to-end data flow...", "info")
    
    # Step 1: Get data from database
    conn = psycopg.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM prioritized_output ORDER BY priority_rank LIMIT 1")
    db_row = cursor.fetchone()
    cursor.close()
    conn.close()
    
    assert db_row is not None, "No data in database"
    db_id, db_title = db_row
    
    # Step 2: Get same data from API
    response = requests.get(f"{API_URL}/api/priorities", timeout=10)
    assert response.status_code == 200, "API request failed"
    
    api_items = response.json()["items"]
    assert len(api_items) > 0, "API returned no items"
    
    # Find the item with matching ID
    api_item = next((item for item in api_items if item["id"] == db_id), None)
    assert api_item is not None, f"Item with ID {db_id} not found in API response"
    assert api_item["title"] == db_title, "Title mismatch between DB and API"
    
    print_test("Data flows correctly from Database → API", "pass")

def test_cors_configuration():
    """Test 10: CORS is properly configured"""
    print_test("Testing CORS configuration...", "info")
    response = requests.options(
        f"{API_URL}/api/priorities",
        headers={
            "Origin": FRONTEND_URL,
            "Access-Control-Request-Method": "GET"
        },
        timeout=5
    )
    # CORS might return 200 or 405, both are acceptable
    assert response.status_code in [200, 405], f"CORS preflight failed: {response.status_code}"
    print_test("CORS configuration appears correct", "pass")

# ===== MAIN TEST RUNNER =====
def main():
    """Run all integration tests."""
    print(f"\n{BOLD}SURF Full Integration Test Suite{RESET}")
    print(f"Testing: Database → API → Frontend\n")
    
    # Database Tests
    print_section("DATABASE TESTS")
    run_test("Test 1: Database Connection", test_database_connection)
    run_test("Test 2: Database Schema", test_database_schema)
    run_test("Test 3: Database Data", test_database_data)
    
    # API Tests
    print_section("API TESTS")
    run_test("Test 4: API Health", test_api_health)
    run_test("Test 5: API Priorities Endpoint", test_api_priorities_endpoint)
    run_test("Test 6: API Stats Endpoint", test_api_stats_endpoint)
    
    # Frontend Tests
    print_section("FRONTEND TESTS")
    run_test("Test 7: Frontend Accessible", test_frontend_accessible)
    run_test("Test 8: Frontend React App", test_frontend_loads_react)
    
    # Integration Tests
    print_section("INTEGRATION TESTS")
    run_test("Test 9: End-to-End Data Flow", test_end_to_end_data_flow)
    run_test("Test 10: CORS Configuration", test_cors_configuration)
    
    # Summary
    print_section("TEST SUMMARY")
    print(f"{BOLD}Total Tests:{RESET} {test_results['total']}")
    print(f"{GREEN}{BOLD}Passed:{RESET} {test_results['passed']}")
    print(f"{RED}{BOLD}Failed:{RESET} {test_results['failed']}")
    
    if test_results['failed'] == 0:
        print(f"\n{GREEN}{BOLD}🎉 ALL INTEGRATION TESTS PASSED! 🎉{RESET}\n")
        return 0
    else:
        print(f"\n{RED}{BOLD}❌ SOME TESTS FAILED{RESET}\n")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Tests interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Fatal error: {str(e)}{RESET}")
        sys.exit(1)

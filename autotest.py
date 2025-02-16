import pytest
import httpx
from pydantic import BaseModel, ValidationError

# Constants
BASE_URL = "https://qa-internship.avito.com"


class PostResponse(BaseModel):
    status: str


class GetResponse(BaseModel):
    id: str
    sellerId: int
    name: str
    price: int
    statistics: dict
    createdAt: str


class StatsResponse(BaseModel):
    likes: int
    viewCount: int
    contacts: int


class ErrorResponse(BaseModel):
    result: dict


# Test setup
@pytest.fixture
def client():
    with httpx.Client(base_url=BASE_URL) as client:
        yield client


# Test cases

# 1. Create Ad
@pytest.mark.parametrize("ad_data", [
    {
        "sellerID": 123433,
        "name": "Another Ad",
        "price": 50,
        "statistics": {
            "contacts": 5,
            "likes": 50,
            "viewCount": 100
        }
    },
    {
        "sellerID": 123650,
        "name": "Aboba@134",
        "price": 50,
        "statistics": {
            "contacts": 5,
            "likes": 50,
            "viewCount": 100
        }
    }
])
def test_create_ad_success(client, ad_data):
    response = client.post("/api/1/item", json=ad_data)
    assert response.status_code == 200
    try:
        PostResponse(**response.json())
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")


@pytest.mark.parametrize("invalid_data", [
    {
        "sellerID": "123433",
        "name": "Another Ad",
        "price": 50,
        "statistics": {
            "contacts": 5,
            "likes": 50,
            "viewCount": 100
        }
    },
    {
        "sellerID": 123678,
        "name": 123,
        "price": 50,
        "statistics": {
            "contacts": 5,
            "likes": 50,
            "viewCount": 100
        }
    },
    {
        "sellerID": 123345,
        "name": "Another Ad",
        "price": "50",
        "statistics": {
            "contacts": 5,
            "likes": 50,
            "viewCount": 100
        }
    },
    {
        "sellerID": 123098,
        "name": "Another Ad",
        "price": 50,
        "statistics": {
            "contacts": "5",
            "likes": 50,
            "viewCount": 100
        }
    },
    {
        "sellerID": 123890,
        "name": "Another Ad",
        "price": 50,
        "statistics": {
            "contacts": 5,
            "likes": "50",
            "viewCount": 100
        }
    },
    {
        "sellerID": 123000,
        "name": "Another Ad",
        "price": 50,
        "statistics": {
            "contacts": 5,
            "likes": 50,
            "viewCount": "100"
        }
    },
    {}
])
def test_create_ad_failure(client, invalid_data):
    response = client.post("/api/1/item", json=invalid_data)
    assert response.status_code == 400
    try:
        error_response = ErrorResponse(**response.json())
        assert "result" in error_response.dict()
        assert isinstance(error_response.result, dict)
        assert "message" in error_response.result
        assert "messages" in error_response.result
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")


# 2. Get Ad by ID
@pytest.mark.parametrize("ad_id", [123456, 457685])
def test_get_ad_success(client, ad_id):
    response = client.get(f"/api/1/item/{ad_id}")
    if response.status_code == 200:
        try:
            GetResponse(**response.json())
        except ValidationError as e:
            pytest.fail(f"Response validation failed: {e}")
    elif response.status_code == 404:
        assert "error" in response.json()
    else:
        pytest.fail(f"Unexpected status code: {response.status_code}")


@pytest.mark.parametrize("ad_id", [None, "abc"])
def test_get_ad_failure(client, ad_id):
    response = client.get(f"/api/1/item/{ad_id}")
    assert response.status_code == 400
    try:
        error_response = ErrorResponse(**response.json())
        assert "result" in error_response.dict()
        assert isinstance(error_response.result, dict)
        assert "message" in error_response.result
        assert "messages" in error_response.result
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")


# 3. Get Ads by SellerID
@pytest.mark.parametrize("seller_id", [265738, 438285])
def test_get_ads_by_seller_success(client, seller_id):
    response = client.get(f"/api/1/{seller_id}/item")
    assert response.status_code == 200
    ads = response.json()
    assert isinstance(ads, list)
    for ad in ads:
        try:
            GetResponse(**ad)
        except ValidationError as e:
            pytest.fail(f"Ad validation failed: {e}")


@pytest.mark.parametrize("seller_id", [None, "abc", 1111111111111111111])
def test_get_ads_by_seller_failure(client, seller_id):
    response = client.get(f"/api/1/{seller_id}/item")
    assert response.status_code == 400
    try:
        error_response = ErrorResponse(**response.json())
        assert "result" in error_response.dict()
        assert isinstance(error_response.result, dict)
        assert "message" in error_response.result
        assert "messages" in error_response.result
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")


# 4. Get Stats by Ad ID
@pytest.mark.parametrize("ad_id", [123456, 234567])
def test_get_stats_success(client, ad_id):
    response = client.get(f"/api/1/statistic/{ad_id}")
    if response.status_code == 200:
        try:
            StatsResponse(**response.json())
        except ValidationError as e:
            pytest.fail(f"Response validation failed: {e}")
    elif response.status_code == 404:
        assert "error" in response.json()
    else:
        pytest.fail(f"Unexpected status code: {response.status_code}")


@pytest.mark.parametrize("ad_id", [None, "abc"])
def test_get_stats_failure(client, ad_id):
    response = client.get(f"/api/1/statistic/{ad_id}")
    assert response.status_code == 400
    try:
        error_response = ErrorResponse(**response.json())
        assert "result" in error_response.dict()
        assert isinstance(error_response.result, dict)
        assert "message" in error_response.result
        assert "messages" in error_response.result
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")

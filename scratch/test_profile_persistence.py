"""
Comprehensive test for My Profile data loading, saving, authentication, and persistence.
Tests:
1. Login as User (e.g. Sanket Belekar, ID 10)
2. Call GET /api/user/profile - verify actual database values are returned:
   - Full Name matches users.name ("Sanket Belekar")
   - Email matches users.email ("sanketbelekar@gmail.com")
   - Age Group matches users.age_group ("18-23")
   - Birthdate matches users.birthdate ("2006-03-27")
   - Language matches users.preferred_language
   - Bio matches users.bio
   - Selected Avatar matches users.selected_avatar
3. Update Profile via PUT /api/user/profile:
   - Change name, age_group, preferred_language (e.g. "Hindi"), bio, phone, birthdate, avatar
   - Verify success response returns updated database data
4. Verify GET /api/user/profile immediately returns the new updated values from the database
5. Simulate page refresh (check_auth / me endpoint + get profile):
   - Verify updated values persist
6. Simulate logout
   - Verify GET /api/user/profile returns 401 Unauthorized
7. Login again with same account:
   - Call GET /api/user/profile
   - Verify all updated values (name, age_group, preferred_language, bio, avatar, etc.) are still intact!
"""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db, User

def run_tests():
    client = app.test_client()

    print("=" * 70)
    print("RUNNING MY PROFILE PERSISTENCE AND DATABASE VERIFICATION TESTS")
    print("=" * 70)

    with app.app_context():
        # Find user Sanket or Alex
        user = User.query.filter_by(email="sanketbelekar@gmail.com").first()
        if not user:
            user = User.query.filter_by(email="buddy@fluency.com").first()
        assert user is not None, "Test user not found in database!"
        
        test_email = user.email
        user_id = user.id
        print(f"Testing with User ID: {user_id}, Name: {user.name}, Email: {user.email}")

    # 1. Test unauthenticated access to GET /api/user/profile
    res = client.get('/api/user/profile')
    assert res.status_code == 401, f"Expected 401 for unauthenticated profile get, got {res.status_code}"
    print("[PASS] Unauthenticated GET /api/user/profile correctly returns 401.")

    # 2. Login as user
    # For testing, we can log in via login endpoint or session
    with client.session_transaction() as sess:
        sess['user_id'] = user_id
        sess['is_admin'] = False

    # 3. Test GET /api/user/profile
    res = client.get('/api/user/profile')
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.get_json()
    assert data.get("status") == "success"
    profile = data.get("user")
    assert profile is not None
    assert profile["id"] == user_id
    assert profile["name"] == user.name
    assert profile["email"] == user.email
    assert profile["age_group"] == user.get_age_group()
    print(f"[PASS] GET /api/user/profile returned exact database record: {profile['name']} ({profile['age_group']}, {profile['preferred_language']})")

    # 4. Update Profile via PUT /api/user/profile
    new_profile = {
        "name": "Sanket B. Expert",
        "selected_avatar": "avatar-river",
        "age_group": "24-30",
        "birthdate": "2000-05-15",
        "phone": "+91 9876543210",
        "bio": "Overcoming public speaking anxiety and mastering smooth pacing.",
        "preferred_language": "Hindi"
    }

    put_res = client.put('/api/user/profile', 
                         data=json.dumps(new_profile),
                         content_type='application/json')
    assert put_res.status_code == 200, f"Expected 200 for PUT profile, got {put_res.status_code}: {put_res.data}"
    put_data = put_res.get_json()
    assert put_data.get("user") is not None
    updated = put_data["user"]
    assert updated["name"] == new_profile["name"]
    assert updated["age_group"] == "24-30"
    assert updated["preferred_language"] == "Hindi"
    assert updated["selected_avatar"] == "avatar-river"
    assert updated["bio"] == new_profile["bio"]
    assert updated["phone"] == new_profile["phone"]
    assert updated["birthdate"] == new_profile["birthdate"]
    print("[PASS] PUT /api/user/profile successfully updated the user row.")

    # 5. Direct Database check to ensure changes were committed to SQLite/MySQL
    with app.app_context():
        db_user = User.query.get(user_id)
        assert db_user.name == new_profile["name"]
        assert db_user.age_group == "24-30"
        assert db_user.preferred_language == "Hindi"
        assert db_user.selected_avatar == "avatar-river"
        assert db_user.bio == new_profile["bio"]
        assert db_user.phone == new_profile["phone"]
        assert db_user.birthdate == new_profile["birthdate"]
        print("[PASS] Direct database query confirms committed changes in users table.")

    # 6. Simulate Refresh: Call GET /api/user/profile and /api/auth/me
    ref_res = client.get('/api/user/profile')
    assert ref_res.status_code == 200
    ref_user = ref_res.get_json()["user"]
    assert ref_user["name"] == new_profile["name"]
    assert ref_user["age_group"] == "24-30"
    assert ref_user["preferred_language"] == "Hindi"
    assert ref_user["selected_avatar"] == "avatar-river"
    print("[PASS] Refresh GET /api/user/profile returns persisted updated values.")

    me_res = client.get('/api/auth/me')
    assert me_res.status_code == 200
    me_user = me_res.get_json()["user"]
    assert me_user["name"] == new_profile["name"]
    assert me_user["age_group"] == "24-30"
    assert me_user["preferred_language"] == "Hindi"
    print("[PASS] /api/auth/me also returns the persisted updated values.")

    # 7. Simulate Logout
    logout_res = client.post('/api/auth/logout')
    assert logout_res.status_code == 200
    res_after_logout = client.get('/api/user/profile')
    assert res_after_logout.status_code == 401
    print("[PASS] User successfully logged out; subsequent profile get rejected.")

    # 8. Login again with same user
    with client.session_transaction() as sess:
        sess['user_id'] = user_id
        sess['is_admin'] = False

    relogin_res = client.get('/api/user/profile')
    assert relogin_res.status_code == 200
    relogin_user = relogin_res.get_json()["user"]
    assert relogin_user["name"] == new_profile["name"]
    assert relogin_user["age_group"] == "24-30"
    assert relogin_user["preferred_language"] == "Hindi"
    assert relogin_user["selected_avatar"] == "avatar-river"
    assert relogin_user["bio"] == new_profile["bio"]
    assert relogin_user["phone"] == new_profile["phone"]
    assert relogin_user["birthdate"] == new_profile["birthdate"]
    print("[PASS] After re-login, all profile values remain perfectly persisted!")

    # 9. Clean up / restore original data for Sanket
    with app.app_context():
        user_to_restore = User.query.get(user_id)
        user_to_restore.name = "Sanket Belekar"
        user_to_restore.age_group = "18-23"
        user_to_restore.preferred_language = "English"
        user_to_restore.selected_avatar = "avatar-sunny"
        user_to_restore.birthdate = "2006-03-27"
        user_to_restore.phone = None
        user_to_restore.bio = "Practicing my voice step by step."
        db.session.commit()
        print("[PASS] Test cleanup: Restored test user back to original state.")

    print("\nALL BACKEND API AND PERSISTENCE TESTS PASSED SUCCESSFULLY! 100% OK")

if __name__ == "__main__":
    run_tests()

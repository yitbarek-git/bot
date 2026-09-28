import os
import unittest
import sqlite3
from app.translations import t, TRANSLATIONS
from app.database.queries import (
    init_db,
    upsert_user,
    get_user_by_telegram_id,
    get_course,
    create_or_update_payment,
    approve_payment,
    reject_payment,
    get_payment_by_id,
    get_student_full_profile,
    get_admin_stats,
    update_user_language,
)


class TestBotTranslations(unittest.TestCase):
    def test_translations_keys_consistency(self):
        """Verify that all keys in English exist in Amharic and format without crashing."""
        en_keys = set(TRANSLATIONS["en"].keys())
        am_keys = set(TRANSLATIONS["am"].keys())
        self.assertEqual(en_keys, am_keys, f"Missing keys: {en_keys ^ am_keys}")

    def test_translation_formatting(self):
        """Verify key string formatting works for placeholders."""
        res_en = t("received_first", "en", payment_id=42)
        self.assertIn("#42", res_en)

        res_am = t("received_first", "am", payment_id=42)
        self.assertIn("#42", res_am)

    def test_default_fallback(self):
        """Verify fallback to English if unknown language code provided."""
        res = t("btn_join_freshman", "unknown_lang")
        self.assertEqual(res, TRANSLATIONS["en"]["btn_join_freshman"])


class TestSqliteDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize test sqlite DB
        init_db("sql/schema.sql")

    def test_course_seeded(self):
        course = get_course("freshman")
        self.assertIsNotNone(course)
        self.assertEqual(course["price"], "400 ETB")
        self.assertEqual(course["telebirr_number"], "0929781996")
        self.assertEqual(course["cbe_number"], "1000316427735")

    def test_student_and_payment_flow(self):
        # 1. Upsert student
        user = upsert_user(
            telegram_id=987654321,
            full_name="Dawit Bekele",
            username="dawit_b",
            language="am",
        )
        self.assertIsNotNone(user)
        self.assertEqual(user["full_name"], "Dawit Bekele")
        self.assertEqual(user["language"], "am")

        # 2. Update language
        update_user_language(987654321, "en")
        user_updated = get_user_by_telegram_id(987654321)
        self.assertEqual(user_updated["language"], "en")

        # 3. Create payment
        payment_id, is_update, count = create_or_update_payment(
            user_id=user["id"],
            course_id="freshman",
            file_type="photo",
            file_id="tg_photo_file_123",
        )
        self.assertFalse(is_update)
        self.assertEqual(count, 1)

        # 4. Fetch payment
        payment = get_payment_by_id(payment_id)
        self.assertIsNotNone(payment)
        self.assertEqual(payment["status"], "pending")

        # 5. Approve payment
        approved = approve_payment(payment_id, "https://t.me/+joinlink123")
        self.assertEqual(approved["status"], "approved")

        # 6. Profile check
        profile = get_student_full_profile(987654321)
        self.assertIsNotNone(profile)
        self.assertEqual(len(profile["enrollments"]), 1)
        self.assertEqual(profile["enrollments"][0]["status"], "active")

        # 7. Admin stats
        stats = get_admin_stats()
        self.assertGreaterEqual(stats["total_users"], 1)
        self.assertGreaterEqual(stats["approved_payments"], 1)


if __name__ == "__main__":
    unittest.main()

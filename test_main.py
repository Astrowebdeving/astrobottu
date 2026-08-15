from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

from main import AstroBotAPIError, get_question, textCheck


class QuestionParsingTests(IsolatedAsyncioTestCase):
    async def test_formats_valid_question(self):
        payload = [
            {
                "title": "Which planet is closest to the Sun?",
                "points": 5,
                "answer": [
                    {"answer": "Venus", "is_correct": False},
                    {"answer": "Mercury", "is_correct": True},
                    {"answer": "Earth", "is_correct": False},
                    {"answer": "Mars", "is_correct": False},
                ],
            }
        ]

        with patch("main.api_get", new=AsyncMock(return_value=payload)):
            question, number, answer, title, points = await get_question()

        self.assertIn("2. Mercury", question)
        self.assertEqual(number, 2)
        self.assertEqual(answer, "Mercury")
        self.assertEqual(title, payload[0]["title"])
        self.assertEqual(points, 5)

    async def test_rejects_question_without_four_answers(self):
        payload = [
            {
                "title": "Incomplete",
                "points": 1,
                "answer": [{"answer": "Only", "is_correct": True}],
            }
        ]

        with patch("main.api_get", new=AsyncMock(return_value=payload)):
            with self.assertRaises(AstroBotAPIError):
                await get_question()

    def test_answer_check(self):
        self.assertEqual(textCheck("2", 2, "Mercury"), (True, "Correct. Mercury is the answer."))
        self.assertEqual(textCheck("1", 2, "Mercury"), (False, "Incorrect."))

from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Answer, Question, Qusers


class RandomQuestionTests(TestCase):
    def make_question(self, title="Active", is_active=True):
        question = Question.objects.create(
            title=title,
            points=5,
            difficulty=1,
            is_active=is_active,
        )
        for index in range(4):
            Answer.objects.create(
                question=question,
                answer=f"Answer {index + 1}",
                is_correct=index == 0,
            )
        return question

    def test_random_endpoint_returns_only_active_questions(self):
        self.make_question(title="Inactive", is_active=False)
        self.make_question(title="Active", is_active=True)

        response = self.client.get(reverse("random"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["title"], "Active")
        self.assertEqual(len(response.json()[0]["answer"]), 4)

    @override_settings(BOT_API_KEY="expected-key")
    def test_random_endpoint_checks_api_key_when_configured(self):
        self.make_question()

        denied = self.client.get(reverse("random"))
        allowed = self.client.get(reverse("random"), HTTP_X_API_KEY="expected-key")

        self.assertEqual(denied.status_code, 403)
        self.assertEqual(allowed.status_code, 200)

    def test_empty_question_bank_returns_empty_list(self):
        response = self.client.get(reverse("random"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


class LeaderboardTests(TestCase):
    def test_top_users_are_ordered_by_points_descending(self):
        Qusers.objects.create(username="low", totalpoints=1)
        Qusers.objects.create(username="high", totalpoints=10)

        response = self.client.get(reverse("top-users"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual([user["username"] for user in response.json()], ["high", "low"])

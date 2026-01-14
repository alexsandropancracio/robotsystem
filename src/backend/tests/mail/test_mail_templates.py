# src/backend/tests/core/mail/test_mail_templates.py

from backend.api.core.mail.mail_templates import activation_email_template


def test_activation_email_template_returns_all_parts():
    subject, text_body, html_body = activation_email_template(
        user_email="user@test.com",
        activation_token="123456"
    )

    assert subject
    assert text_body
    assert html_body


def test_activation_email_template_contains_token():
    token = "ABC123"

    _, text_body, html_body = activation_email_template(
        user_email="user@test.com",
        activation_token=token
    )

    assert token in text_body
    assert token in html_body


def test_activation_email_template_contains_user_email():
    email = "user@test.com"

    _, text_body, html_body = activation_email_template(
        user_email=email,
        activation_token="123456"
    )

    assert email in text_body
    assert email in html_body


def test_activation_email_template_subject_contains_app_name():
    subject, _, _ = activation_email_template(
        user_email="user@test.com",
        activation_token="123456",
        app_name="RobotSystem"
    )

    assert "RobotSystem" in subject


def test_activation_email_template_custom_expiration_time():
    _, text_body, html_body = activation_email_template(
        user_email="user@test.com",
        activation_token="123456",
        expires_minutes=30
    )

    assert "30" in text_body
    assert "30" in html_body

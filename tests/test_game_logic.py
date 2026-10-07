import random

from streamlit.testing.v1 import AppTest

from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_hint_direction_matches_outcome():
    # Regression test: HINT_MESSAGES used to tell the player to go the
    # wrong direction (e.g. "Too High" paired with "Go HIGHER!").
    from app import HINT_MESSAGES

    too_high_outcome = check_guess(60, 50)
    too_low_outcome = check_guess(40, 50)

    assert "LOWER" in HINT_MESSAGES[too_high_outcome].upper()
    assert "HIGHER" in HINT_MESSAGES[too_low_outcome].upper()


def test_new_game_starts_with_zero_attempts_used():
    # Regression test: a freshly started game used to begin with
    # attempts=1, eating into the attempt limit before any guess was made.
    at = AppTest.from_file("app.py")
    at.run()

    assert at.session_state["attempts"] == 0


def test_instructions_show_selected_difficulty_range():
    # Regression test: the instructions used to always say
    # "between 1 and 100" no matter which difficulty was selected.
    at = AppTest.from_file("app.py")
    at.run()

    at.sidebar.selectbox[0].select("Easy").run()

    assert "between 1 and 20" in at.info[0].value
    assert "between 1 and 100" not in at.info[0].value


def test_new_game_uses_difficulty_range_for_secret(monkeypatch):
    # Regression test: New Game used to hardcode random.randint(1, 100)
    # instead of using the selected difficulty's (low, high) range.
    calls = []
    original_randint = random.randint

    def recording_randint(low, high):
        calls.append((low, high))
        return original_randint(low, high)

    monkeypatch.setattr(random, "randint", recording_randint)

    at = AppTest.from_file("app.py")
    at.run()
    at.sidebar.selectbox[0].select("Hard").run()

    new_game_button = at.button[1]
    assert new_game_button.label == "New Game \U0001f501"
    new_game_button.click().run()

    assert calls[-1] == (1, 50)


def test_new_game_resets_attempts_score_status_and_history():
    # Regression test: New Game used to only reset attempts/secret,
    # leaving score, status, and history stuck from the previous game.
    at = AppTest.from_file("app.py")
    at.run()

    at.session_state["attempts"] = 4
    at.session_state["score"] = 55
    at.session_state["status"] = "won"
    at.session_state["history"] = [1, 2, 3]
    at.run()

    new_game_button = at.button[1]
    assert new_game_button.label == "New Game \U0001f501"
    new_game_button.click().run()

    assert at.session_state["attempts"] == 0
    assert at.session_state["score"] == 0
    assert at.session_state["status"] == "playing"
    assert at.session_state["history"] == []

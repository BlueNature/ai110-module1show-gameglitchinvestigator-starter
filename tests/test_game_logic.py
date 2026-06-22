from logic_utils import (
    check_guess,
    update_score,
    get_range_for_difficulty,
    parse_guess,
)


# --- check_guess ---

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

def test_winning_guess_off_boundary():
    outcome, message = check_guess(1, 1)
    assert outcome == "Win"

def test_guess_one_above_is_too_high():
    outcome, _ = check_guess(51, 50)
    assert outcome == "Too High"

def test_guess_one_below_is_too_low():
    outcome, _ = check_guess(49, 50)
    assert outcome == "Too Low"

def test_negative_numbers_compare_correctly():
    assert check_guess(-3, -5)[0] == "Too High"
    assert check_guess(-5, -3)[0] == "Too Low"

def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

def test_hint_too_high_says_go_lower():
    # Bug fix: when guess > secret the hint must say go LOWER, not HIGHER
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message
    assert "HIGHER" not in message

def test_hint_too_low_says_go_higher():
    # Bug fix: when guess < secret the hint must say go HIGHER, not LOWER
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message
    assert "LOWER" not in message


# --- update_score ---

def test_win_awards_points():
    score = update_score(0, "Win", 1)
    assert score > 0

def test_win_score_decreases_with_more_attempts():
    early = update_score(0, "Win", 1)
    late = update_score(0, "Win", 5)
    assert early > late

def test_win_score_never_below_10_bonus():
    # Even on attempt 100 the bonus floors at 10
    score = update_score(0, "Win", 100)
    assert score == 10

def test_too_high_subtracts_points():
    # Bug fix: "Too High" should always subtract, never add
    score = update_score(50, "Too High", 2)
    assert score < 50

def test_too_high_odd_attempt_subtracts():
    score = update_score(50, "Too High", 3)
    assert score < 50

def test_too_low_subtracts_points():
    score = update_score(50, "Too Low", 1)
    assert score < 50

def test_unknown_outcome_unchanged():
    score = update_score(42, "Unknown", 1)
    assert score == 42

def test_too_high_and_too_low_subtract_same_amount():
    assert update_score(50, "Too High", 1) == update_score(50, "Too Low", 1)

def test_win_on_first_attempt_awards_100():
    # Off-by-two fix: winning on attempt 1 earns the full 100 points
    score = update_score(0, "Win", 1)
    assert score == 100

def test_win_adds_to_existing_score():
    score = update_score(25, "Win", 1)
    assert score == 125

def test_subtracting_can_go_negative():
    score = update_score(0, "Too High", 1)
    assert score == -5

def test_empty_outcome_unchanged():
    score = update_score(42, "", 1)
    assert score == 42


# --- get_range_for_difficulty ---

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    # Bug fix: Normal must be 1-50, not swapped with Hard
    assert get_range_for_difficulty("Normal") == (1, 50)

def test_hard_range():
    # Bug fix: Hard must be 1-100, not swapped with Normal
    assert get_range_for_difficulty("Hard") == (1, 100)

def test_unknown_difficulty_defaults_to_hard_range():
    assert get_range_for_difficulty("Impossible") == (1, 100)

def test_difficulty_is_case_sensitive():
    # Lowercase is not recognized and falls back to the default
    assert get_range_for_difficulty("easy") == (1, 100)


# --- parse_guess ---

def test_parse_valid_integer():
    ok, value, error = parse_guess("42")
    assert ok is True
    assert value == 42
    assert error is None

def test_parse_negative_integer():
    ok, value, error = parse_guess("-7")
    assert ok is True
    assert value == -7

def test_parse_float_string_truncates():
    ok, value, error = parse_guess("3.9")
    assert ok is True
    assert value == 3

def test_parse_none_returns_error():
    ok, value, error = parse_guess(None)
    assert ok is False
    assert value is None
    assert error == "Enter a guess."

def test_parse_empty_string_returns_error():
    ok, value, error = parse_guess("")
    assert ok is False
    assert error == "Enter a guess."

def test_parse_non_numeric_returns_error():
    ok, value, error = parse_guess("abc")
    assert ok is False
    assert value is None
    assert error == "That is not a number."

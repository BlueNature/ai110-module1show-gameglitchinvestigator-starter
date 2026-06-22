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


# --- parse_guess: difficult edge cases ---

def test_parse_surrounding_whitespace_is_stripped():
    # int() tolerates surrounding whitespace
    ok, value, error = parse_guess("  42  ")
    assert ok is True
    assert value == 42
    assert error is None

def test_parse_whitespace_only_is_not_a_number():
    # A non-empty string of only spaces is NOT caught by the "" check,
    # so it must fall through to the int() parse and fail.
    ok, value, error = parse_guess("   ")
    assert ok is False
    assert value is None
    assert error == "That is not a number."

def test_parse_leading_plus_sign():
    ok, value, error = parse_guess("+5")
    assert ok is True
    assert value == 5

def test_parse_underscore_separated_int():
    # Python's int() accepts digit-group underscores.
    ok, value, error = parse_guess("1_000")
    assert ok is True
    assert value == 1000

def test_parse_scientific_notation_fails_without_dot():
    # "1e3" has no ".", so it goes through int("1e3") which raises.
    ok, value, error = parse_guess("1e3")
    assert ok is False
    assert value is None
    assert error == "That is not a number."

def test_parse_negative_float_truncates_toward_zero():
    # int(float(...)) truncates toward zero, NOT floor: -3.9 -> -3, not -4.
    ok, value, error = parse_guess("-3.9")
    assert ok is True
    assert value == -3

def test_parse_leading_dot_float():
    ok, value, error = parse_guess(".75")
    assert ok is True
    assert value == 0

def test_parse_trailing_dot_float():
    ok, value, error = parse_guess("5.")
    assert ok is True
    assert value == 5

def test_parse_negative_leading_dot_truncates_to_zero():
    # -0.9 truncates toward zero -> 0
    ok, value, error = parse_guess("-0.9")
    assert ok is True
    assert value == 0

def test_parse_multiple_dots_fails():
    # "10.5.5" has a ".", so float("10.5.5") is attempted and raises.
    ok, value, error = parse_guess("10.5.5")
    assert ok is False
    assert value is None
    assert error == "That is not a number."

def test_parse_dot_only_fails():
    ok, value, error = parse_guess(".")
    assert ok is False
    assert error == "That is not a number."


# --- update_score: difficult edge cases ---

def test_win_floor_boundary_attempt_10_is_exactly_10():
    # attempt 10: 100 - 10*9 = 10, the bonus is exactly 10 with no flooring.
    assert update_score(0, "Win", 10) == 10

def test_win_floor_boundary_attempt_11_floors_to_10():
    # attempt 11: 100 - 10*10 = 0, which is below 10 and floors up to 10.
    assert update_score(0, "Win", 11) == 10

def test_win_just_above_floor_attempt_9_awards_20():
    # attempt 9: 100 - 10*8 = 20, the last value before the floor kicks in.
    assert update_score(0, "Win", 9) == 20

def test_win_floor_applies_even_with_existing_score():
    # The 10-point floor is on the awarded points, then added to current.
    assert update_score(55, "Win", 50) == 65

def test_wrong_guess_from_negative_score_goes_more_negative():
    assert update_score(-5, "Too High", 3) == -10


# --- full-workflow sequences ---

def test_full_workflow_parse_then_win():
    # Parse a raw input, confirm difficulty range, check the guess, score it.
    low, high = get_range_for_difficulty("Normal")
    assert (low, high) == (1, 50)

    ok, guess, error = parse_guess(" 50 ")
    assert ok is True and error is None
    assert low <= guess <= high

    outcome, message = check_guess(guess, 50)
    assert outcome == "Win"

    score = update_score(0, outcome, 1)
    assert score == 100

def test_full_workflow_misses_then_win_accumulates_score():
    # Two wrong guesses (-5 each) then a win on attempt 3 (100 - 20 = 80).
    secret = 30
    score = 0

    ok, g1, _ = parse_guess("40")
    out1, _ = check_guess(g1, secret)
    assert out1 == "Too High"
    score = update_score(score, out1, 1)
    assert score == -5

    ok, g2, _ = parse_guess("3.9")  # truncates to 3, still too low
    out2, _ = check_guess(g2, secret)
    assert out2 == "Too Low"
    score = update_score(score, out2, 2)
    assert score == -10

    ok, g3, _ = parse_guess("30")
    out3, _ = check_guess(g3, secret)
    assert out3 == "Win"
    score = update_score(score, out3, 3)
    # -10 + (100 - 10*2) = -10 + 80 = 70
    assert score == 70

def test_full_workflow_invalid_input_does_not_advance_score():
    # A bad parse should never reach check_guess/update_score; score holds.
    score = 42
    ok, guess, error = parse_guess("not-a-number")
    assert ok is False
    assert guess is None
    assert error == "That is not a number."
    # Caller skips scoring on a failed parse.
    if ok:
        outcome, _ = check_guess(guess, 10)
        score = update_score(score, outcome, 1)
    assert score == 42

def test_full_workflow_hard_difficulty_upper_boundary_win():
    low, high = get_range_for_difficulty("Hard")
    assert (low, high) == (1, 100)

    ok, guess, _ = parse_guess("100")
    assert ok is True
    assert guess == high

    outcome, _ = check_guess(guess, 100)
    assert outcome == "Win"
    # Win on attempt 5: 100 - 10*4 = 60
    assert update_score(0, outcome, 5) == 60

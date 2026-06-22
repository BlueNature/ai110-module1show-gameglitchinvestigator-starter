from logic_utils import check_guess, update_score


# --- check_guess ---

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

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

# FIX: Refactored logic into logic_utils.py using agent mode

# FIX: Swapped difficulty range for normal and hard
def get_range_for_difficulty(difficulty: str):
    """Return the inclusive guessing range for a difficulty level.

    Args:
        difficulty: The difficulty name. Recognized values are
            "Easy", "Normal", and "Hard".

    Returns:
        A (low, high) tuple of ints giving the inclusive bounds for
        the secret number. Easy is 1-20, Normal is 1-50, and Hard is
        1-100. Any unrecognized value defaults to the 1-100 range.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
    """Parse raw user input into an integer guess.

    Accepts plain integer strings as well as decimal strings, which are
    truncated toward zero (e.g. "3.9" becomes 3).

    Args:
        raw: The raw input string from the user, or None.

    Returns:
        A (ok, guess, error) tuple where ``ok`` is True only when parsing
        succeeded. On success, ``guess`` is the parsed int and ``error`` is
        None. On failure, ``guess`` is None and ``error`` is a
        user-facing message explaining the problem.
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare a guess against the secret number.

    Args:
        guess: The player's guessed integer.
        secret: The secret integer the player is trying to find.

    Returns:
        An (outcome, message) tuple. ``outcome`` is "Win" when the guess
        matches, "Too High" when the guess exceeds the secret, and
        "Too Low" otherwise. ``message`` is a user-facing hint string for
        that outcome.
    """
    # FIX: Removed dead/buggy except TypeError fallback that did lexicographic
    # string comparison; secret and guess are always ints now
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


# FIX: Fixed off-by-two error for calculating points won after guessing
# correctly (interpreting as winning on first guess earns 100)
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Compute the new score after a single guess.

    A win awards 100 points on the first attempt, decreasing by 10 for
    each subsequent attempt down to a floor of 10. A wrong guess
    ("Too High" or "Too Low") costs 5 points. These are the only
    outcomes :func:`check_guess` produces; an unrecognized outcome is
    treated defensively and leaves the score unchanged.

    Args:
        current_score: The player's score before this guess.
        outcome: The result of the guess, as returned by
            :func:`check_guess` (i.e. "Win", "Too High", or "Too Low").
        attempt_number: The 1-based number of the current attempt.

    Returns:
        The updated score as an int.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score

import block_letters

def are_isomorphic (s: str, t: str) -> bool:
    """Determine whether two strings are isomorphic using plain lists."""

    min_length = 1
    max_length = 500
    invalid_index = -1

    valid = True

    # Check that both inputs are strings.
    if not isinstance(s, str) or not isinstance(t, str):
        valid = False

    # Check the required lengths.
    if valid:
        if len(s) < min_length or len(s) > max_length:
            valid = False
        elif len(t) != len(s):
            valid = False

    # Make sure every character is a letter.
    if valid:
        for char in s:
            if not char.isalpha():
                valid = False

    if valid:
        for char in t:
            if not char.isalpha():
                valid = False

    s_seen: list[str] = []
    t_seen: list[str] = []

    if valid:
        for i in range(len(s)):
            char_s = s[i]
            char_t = t[i]

            s_idx = invalid_index

            # Find the position where char_s was first seen.
            for idx in range(len(s_seen)):
                if s_seen[idx] == char_s and s_idx == invalid_index:
                    s_idx = idx

            t_idx = invalid_index

            # Find the position where char_t was first seen.
            for idx in range(len(t_seen)):
                if t_seen[idx] == char_t and t_idx == invalid_index:
                    t_idx = idx

            # Previously seen characters must have matching positions.
            if s_idx != invalid_index and t_idx != invalid_index:
                if s_idx != t_idx:
                    valid = False

            # New characters must both be new.
            elif s_idx == invalid_index and t_idx == invalid_index:
                s_seen.append(char_s)
                t_seen.append(char_t)

            # Only one character being new means the mapping is invalid.
            else:
                valid = False

    return valid


def contiguous_length(nums: list[int]) -> int:
    """Find the longest contiguous binary subarray with equal 0s and 1s."""

    min_length = 1
    max_length = 2000
    zero = 0
    one = 1

    result = 0
    valid = True

    # Check that the input is a list.
    if not isinstance(nums, list):
        valid = False

    # Check the list length.
    if valid:
        if len(nums) < min_length or len(nums) > max_length:
            valid = False

    # Check that every item is exactly 0 or 1.
    if valid:
        for num in nums:
            if not isinstance(num, int) or isinstance(num, bool):
                valid = False
            elif num != zero and num != one:
                valid = False

    # Search every possible contiguous subarray.
    if valid:
        n = len(nums)

        for start in range(n):
            zeros = 0
            ones = 0

            for end in range(start, n):
                if nums[end] == zero:
                    zeros += 1
                else:
                    ones += 1

                if zeros == ones:
                    length = end - start + 1

                    if length > result:
                        result = length

    return result


def mirror_letters(letters: list[list[str]]) -> list[list[str]] | None:
    """Mirror block letters left-to-right and reverse their order."""

    result: list[list[str]] | None = None
    valid = True

    # The input itself must be a list.
    if not isinstance(letters, list):
        valid = False

    if valid and len(letters) == 0:
        result = []

    expected_rows = None
    expected_width = None

    # Validate the dimensions and row types.
    if valid and len(letters) > 0:
        for letter in letters:
            if not isinstance(letter, list):
                valid = False

            if valid:
                if expected_rows is None:
                    expected_rows = len(letter)
                elif len(letter) != expected_rows:
                    valid = False

            if valid:
                for row in letter:
                    if not isinstance(row, str):
                        valid = False

                    if valid:
                        if expected_width is None:
                            expected_width = len(row)
                        elif len(row) != expected_width:
                            valid = False

    # Build the mirrored word if the input is valid.
    if valid and result is None:
        mirrored_word: list[list[str]] = []

        for letter_idx in range(len(letters) - 1, -1, -1):
            letter = letters[letter_idx]
            mirrored_letter: list[str] = []

            for row in letter:
                reversed_row = ""

                # Manually reverse each row.
                for char_idx in range(len(row) - 1, -1, -1):
                    reversed_row += row[char_idx]

                mirrored_letter.append(reversed_row)

            mirrored_word.append(mirrored_letter)

        result = mirrored_word

    return result

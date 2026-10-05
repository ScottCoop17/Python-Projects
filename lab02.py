def caesar_encrypt(plaintext, shift):
    result = ""
    shift = shift % 26

    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                new_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))

            result += new_char
        else:
            # Keep spaces and punctuation unchanged
            result += char

    return result


def caesar_decrypt(ciphertext, shift):
    return caesar_encrypt(ciphertext, -shift)



def rail_fence_encrypt(plaintext, rails):
    # If there is only one rail, no encryption happens
    if rails <= 1 or rails >= len(plaintext):
        return plaintext

    # Create empty rails
    fence = [""] * rails

    rail = 0
    direction = 1

    # Place characters in zig-zag pattern
    for char in plaintext:
        fence[rail] += char

        # Change direction at top and bottom
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1

        rail += direction

    # Read each rail from top to bottom
    return "".join(fence)


def rail_fence_decrypt(ciphertext, rails):
    # If there is only one rail, no decryption happens
    if rails <= 1 or rails >= len(ciphertext):
        return ciphertext

    length = len(ciphertext)

    # Figure out which rail each character belongs to
    pattern = []
    rail = 0
    direction = 1

    for i in range(length):
        pattern.append(rail)

        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1

        rail += direction

    # Count how many characters belong in each rail
    rail_counts = [pattern.count(r) for r in range(rails)]

    # Split ciphertext into the correct rails
    fence = []
    index = 0

    for count in rail_counts:
        fence.append(list(ciphertext[index:index + count]))
        index += count

    # Rebuild the original message using the zig-zag pattern
    result = ""
    rail_positions = [0] * rails

    for rail in pattern:
        result += fence[rail][rail_positions[rail]]
        rail_positions[rail] += 1

    return result


print("===== CAESAR CIPHER TESTS =====")

print(caesar_encrypt("ATTACK AT DAWN", 5))

print(caesar_decrypt("FXXF?K?F?I?", 5))

print(caesar_encrypt("COMP301", 7))

print(caesar_decrypt(caesar_encrypt("COMP301", 7), 7))


print("\n===== RAIL FENCE CIPHER TESTS =====")

print(rail_fence_encrypt("HELLO WORLD", 3))

print(rail_fence_decrypt("HOLEL WDLRO", 3))

print(rail_fence_encrypt("SECRETSHARED", 4))

print(rail_fence_decrypt(
    rail_fence_encrypt("SECRETSHARED", 4), 4
))

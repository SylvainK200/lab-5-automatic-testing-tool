def test_strong_password_checker(strong_password_checker):
    assert strong_password_checker("a") == 5
    assert strong_password_checker("aA1") == 3
    assert strong_password_checker("1337C0d3") == 0
    assert strong_password_checker("aaaB1") == 1  # Needs one uppercase or digit
    assert strong_password_checker("A123456789012345678901") == 1  # Too long
    assert strong_password_checker("aaaaaaaaaaaaaaaaaaaaa") == 7  # Too long, needs variety, repeating chars
    assert strong_password_checker("ABABABABABABABABABAB1") == 2 # Needs lowercase, repeating chars
    assert strong_password_checker("abcdefghijklmnopqrstuvwxyz") == 3 # Needs digit, uppercase, too long
    assert strong_password_checker("") == 6 # Empty string
    assert strong_password_checker("bbaaaaaaaaaaaaaaacccccc") == 8 # Repeating chars, too long
    assert strong_password_checker("..................!!!") == 7 # Needs alphanumeric, too long
    assert strong_password_checker("1Abababcabababc") == 2 # Repeating chars
    assert strong_password_checker("1111111111") == 3 # Repeating chars, needs uppercase & lowercase

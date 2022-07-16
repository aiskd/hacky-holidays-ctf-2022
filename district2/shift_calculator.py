LETTERS = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

while True:
    coded = input("Input coded message: ").lower()
    decoded = input("Input decoded message: ").lower()
    if len(coded) != len(decoded):
        print("ERROR: coded and decoded messages must be of same length")
        continue

    for i in range(len(coded)):
        c_letter = coded[i]
        d_letter = decoded[i]
        if coded[i] in LETTERS and decoded[i] in LETTERS:
            c_index = LETTERS.index(c_letter)
            d_index = LETTERS.index(d_letter)
            print(f"distance between {c_letter} ({c_index:2.0f}) and {d_letter} ({d_index:2.0f}): {c_index - d_index:}")
        else:
            print(c_letter if c_letter == d_letter else f"{c_letter}, {d_letter}")

from sympy import randprime

def find_public_exponent(totient):
    e = 3
    while e <= 65537:
        a = totient
        b = e
        while b: 
            a, b = b, a % b
        if a == 1:
            return e
        else:
            e += 2
    print("Cannot find exponent!")

def extended_euclidean_algorithm(a, b): # greatest common divisor for a and b
    if a == 0:
        return b, 0, 1
    else:
        gcd, x1, y1 = extended_euclidean_algorithm(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

def modular_inverse(e, totient): # calculates d by checking formula: (d*e) mod totient = 1
    gcd, x, y = extended_euclidean_algorithm(e, totient)
    if gcd != 1:
        print('Mod inverse does not exist!')
    else:
        return x % totient

def generateKeys():
    # Random two large prime numbers (2048 bits)
    prime1 = randprime(2**2047, 2**2048)
    prime2 = randprime(2**2047, 2**2048)
    n = prime1 * prime2
    totient = (prime1-1) * (prime2-1)
    
    e = find_public_exponent(totient)
    d = modular_inverse(e, totient)

    with open("public.txt", "w") as pub_file:
        pub_file.write(f"{n}\n")
        pub_file.write(f"{e}\n")
    with open("private.txt", "w") as priv_file:
        priv_file.write(f"{n}\n")
        priv_file.write(f"{d}\n")
    print("Keys generated")

def read_key(filename):
    with open(filename, "r") as file:
        n = int(file.readline().strip())
        exponent = int(file.readline().strip())
    return n, exponent

def encrypt(message, e, n):
    m = int.from_bytes(message.encode(), 'big')
    return pow(m, e, n)

def decrypt(encryptedMessage, d, n):
    m = pow(encryptedMessage, d, n)
    message = m.to_bytes((m.bit_length() + 7) // 8, "big").decode("utf-8")
    return message


def menu():
    print(
    """
    [1] Encrypt a message
    [2] Decpyrt
    [3] Generate keys
    [4] Exit
    """
    )
    public_key = "public.txt"
    private_key = "private.txt"
    try:
        menuInput = int(input("Choose an option: "))
    except ValueError:
        print("Invalid input. Enter a number!")
        menu()
        return
    
    match menuInput:
        case 1: 
            messageInput = (input("Write a message: "))
            n, e = read_key(public_key)
            encrypted = encrypt(messageInput, e, n)
            print(f"encrypted message: {encrypted}")
            menu()
        case 2:
            messageInput = int(input("Write a message: "))
            n, e = read_key(private_key)
            decrypted = decrypt(messageInput, e, n)
            print(f"decrypted message: {decrypted}")
            menu()
        case 3:
            generateKeys()
            menu()
        case 4:
            exit
        case _:
            menu()

if __name__ == "__main__":
    menu()

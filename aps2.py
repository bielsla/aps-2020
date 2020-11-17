import random
def rabinMiller(n, d):
    a = random.randint(2, (n - 2) - 2)
    x = pow(a, int(d), n)  # a^d%n
    if x == 1 or x == n - 1:
        return True

    # quadrado de x
    while d != n - 1:
        x = pow(x, 2, n)
        d *= 2
        if x == 1:
            return False
        elif x == n - 1:
            return True

    # não é primo
    return False


def isPrime(n):
    '''
        retorna verdadeiro se n for número primo
        retorna para o rabbinMiller se for incorreto
    '''
    # 0,1 não são primo
    if n < 2:
        return False
    # Os menores números primo para poupar tempo
    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    # se estiver em lowPrimes
    if n in lowPrimes:
        return True
    # se lowPrimes divide por n
    for prime in lowPrimes:
        if n % prime == 0:
            return False
    # encontra número de c de modo que c * 2 ^ r = n -1
    c = n - 1  # c até por que n não é divisivel por 2
    while c % 2 == 0:
        c /= 2  # transforma c em ímpar
    # prova que não é primo 128 vezes
    for i in range(128):
        if not rabinMiller(n, c):
            return False
    return True


def generateKeys(keysize=1024):
    e = d = n = 0
    # gera números primo, p e q
    p = generateLargePrime(keysize)
    q = generateLargePrime(keysize)
    '''
    print('Números primo: ')
    print('-----------------------')
    print(f'p: {p}')
    print(f'q: {q}')
    print('-----------------------')
    '''
    n = p * q  # Módulo RSA
    phiN = (p - 1) * (q - 1)  # Totiente de Euler
    # escolhe e
    # e é coprime com phiN & 1 < e <= phiN
    while True:
        e = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
        if (isCoPrime(e, phiN)):
            break
    # escolhe d
    # d é mod inv de e respeitando phiN, e * d (mod phiN) = 1
    d = moduloInv(e, phiN)
    return e, d, n


def generateLargePrime(keysize):
    '''
        retorna um grande número aleatório do tamanho da keysize em bits
    '''
    while True:
        num = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
        if (isPrime(num)):
            return num


def isCoPrime(p, q):
    '''
        retorna verdadeiro se gcd(p,q) for 1
        relativamente primo
    '''

    return gcd(p, q) == 1


def gcd(p, q):
    """
        Algoritmo de Euclidean para achar o máximo divisor comum de p e q
    """
    while q:
        p, q = q, p % q
    return p


def egcd(a, b):
    s = 0
    old_s = 1
    t = 1
    old_t = 0
    r = b
    old_r = a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def moduloInv(a, b):
    gcd, x, y = egcd(a, b)

    if x < 0:
        x += b

    return x


def encrypt(e, n, msg):
    cipher = ""
    for c in msg:
        m = ord(c)
        cipher += str(pow(m, e, n)) + " "

    return cipher


def decrypt(d, n, cipher):
    msg = ""

    parts = cipher.split()
    for part in parts:
        if part:
            c = int(part)
            msg += chr(pow(c, d, n))

    return msg


keysize = 32
e, d, n = generateKeys(keysize)

print('-------------------------------')
print('ESSE PROJETO FOI DESENVOLVIDO')
print('PARA RESTRINGIR O ACESSO DE UMA')
print('ÁREA CONTAMINADA AMBIENTALMENTE')
print('-------------------------------')
while True:
    msg = ''
    opcao = 0
    chave = 0
    print('Bem Vindo!')
    print('Menu RSA: \n1- Criptografar \n2- Descriptografar \n0- Sair ')
    opcao = int(input(''))
    if (opcao == 1):
        msg = input('Digite o que deseja criptografar: ')
        enc = encrypt(e, n, msg)
        print(f'Mensagem criptografada: {enc}')
        print(f'Sua chave para descriptografar essa mensagem é {d}')
    elif (opcao == 2):
        chave = int(input('Informe sua chave: '))
        if (chave == d):
            dec = decrypt(d, n, enc)
            print(f'Mensagem descriptografada: {dec}')
        else:
            print('Chave incorreta!')
    elif (opcao == 0):
        print('Obrigado por utilizar')
        break

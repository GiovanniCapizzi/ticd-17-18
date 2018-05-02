# coding=utf-8
from collections import defaultdict


def primes():
    """Yields the sequence of primes via the Sieve of Eratosthenes."""
    yield 2  # Only even prime.  Sieve only odd numbers.

    # Generate recursively the sequence of primes up to sqrt(n).
    # Each p from the sequence is used to initiate sieving at p*p.
    roots = primes()
    root = next(roots)
    square = root * root

    # The main sieving loop.
    # We use a hash table D such that D[n]=2p for p a prime factor of n.
    # Each prime p up to sqrt(n) appears once as a value in D, and is
    # moved to successive odd multiples of p as the sieve progresses.
    D = {}
    n = 3
    while True:
        if n >= square:  # Time to include another square?
            D[square] = root + root
            root = next(roots)
            square = root * root

        if n not in D:  # Not witnessed, must be prime.
            yield n
        else:  # Move witness p to next free multiple.
            p = D[n]
            q = n + p
            while q in D:
                q += p
            del D[n]
            D[q] = p
        n += 2  # Move on to next odd number.


def FactoredIntegers():
    """
    Generate pairs n,F where F is the prime factorization of n.
    F is represented as a dictionary in which each prime factor of n
    is a key and the exponent of that prime is the corresponding value.
    """
    yield 1, {}
    i = 2
    factorization = defaultdict(dict)
    while True:
        if i not in factorization:  # prime
            F = {i: 1}
            yield i, F
            factorization[2 * i] = F
        elif len(factorization[i]) == 1:  # prime power
            p, x = next(iter(factorization[i].items()))
            F = {p: x + 1}
            yield i, F
            factorization[2 * i] = F
            factorization[i + p ** x][p] = x
            del factorization[i]
        else:
            yield i, factorization[i]
            for p, x in factorization[i].items():
                q = p ** x
                iq = i + q
                if iq in factorization and p in factorization[iq]:
                    iq += p ** x  # skip higher power of p
                factorization[iq][p] = x
            del factorization[i]
        i += 1


def MoebiusSequence():
    """The sequence of values of the Moebius function, OEIS A008683."""
    for n, F in FactoredIntegers():
        if n > 1 and set(F.values()) != {1}:
            yield 0
        else:
            yield (-1) ** len(F)


MoebiusFunctionValues = [None]
MoebiusFunctionIterator = MoebiusSequence()


def MoebiusFunction(n):
    """A functional version of the Moebius sequence.
    Efficient only for small values of n."""
    while n >= len(MoebiusFunctionValues):
        MoebiusFunctionValues.append(next(MoebiusFunctionIterator))
    return MoebiusFunctionValues[n]


def isPracticalFactorization(f):
    """Test whether f is the factorization of a practical number."""
    f = sorted(f.items())
    sigma = 1
    for p, x in f:
        if sigma < p - 1:
            return False
        sigma *= (p ** (x + 1) - 1) // (p - 1)
    return True


def PracticalNumbers():
    """Generate the sequence of practical (or panarithmic) numbers."""
    for x, f in FactoredIntegers():
        if isPracticalFactorization(f):
            yield x


if __name__ == "__main__":
    pass

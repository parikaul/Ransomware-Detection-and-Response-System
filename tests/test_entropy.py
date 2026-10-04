from app.core.entropy import shannon_entropy
def test_empty(): assert shannon_entropy(b"")==0
def test_constant(): assert shannon_entropy(b"a"*100)<0.01
def test_random_like(): assert shannon_entropy(bytes(range(256))*4)>7.9

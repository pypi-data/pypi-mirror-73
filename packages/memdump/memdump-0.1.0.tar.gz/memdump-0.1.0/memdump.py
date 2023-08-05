import io

ASCII = b'.' * 32 + bytes(range(32, 127)) + b'.' * 129


def dump(data, n=16, base=0):
    res = io.StringIO()
    for i in range(0, len(data), n):
        row = data[i : i + n].hex() + '  ' * n
        left = ' '.join(row[k : k + 2] for k in range(0, n, 2))
        right = ' '.join(row[k : k + 2] for k in range(n, n * 2, 2))
        text = data[i : i + 16].translate(ASCII).decode()
        res.write(f'{base + i:08x} | {left} | {right} | {text}\n')
    return res.getvalue()

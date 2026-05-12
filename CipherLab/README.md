# CipherLab

> A browser-based cryptography toolkit built with pure HTML, CSS, and JavaScript — no frameworks, no dependencies.

---

## What It Does

CipherLab contains two security tools:

### 1. Caesar Cipher
Encrypts and decrypts text using the Caesar cipher — one of the oldest known encryption techniques. A shift value (1–25) moves each letter forward or backward in the alphabet.

- Adjustable shift slider (1–25)
- Encrypts and decrypts any text
- Preserves spaces, numbers, and punctuation
- **Brute Force demo** — reveals all 25 possible decryptions at once, showing why Caesar cipher is completely insecure

### 2. Password Strength Analyzer
Analyzes a password in real time against 6 security criteria:

| Criterion | Rule |
|-----------|------|
| Length | 12+ characters |
| Uppercase | At least one A–Z |
| Lowercase | At least one a–z |
| Number | At least one 0–9 |
| Special character | At least one symbol |
| Not common | Not in the common password blocklist |

Each criterion lights up as it passes. A strength bar and score (0–6) update live as you type.

---

## How to Run It

No installation required.

1. Download `index.html`
2. Double-click it — it opens directly in any browser
3. No internet connection needed after the font loads

---

## Security Concepts Demonstrated

| Concept | Where |
|---------|-------|
| Substitution cipher | Caesar Cipher tool |
| Why simple ciphers fail | Brute Force demo — all 25 shifts shown instantly |
| Password entropy | Strength Analyzer — 6-criteria scoring |
| Common password attacks | Blocklist check against known weak passwords |

---

## Code Concepts Used

| Concept | Used For |
|---------|----------|
| Functions | `caesarCipher()`, `analyzePassword()` |
| String methods | `.split()`, `.map()`, `.join()` |
| ASCII arithmetic | Shifting letters using `charCodeAt()` and `fromCharCode()` |
| Modulo operator `%` | Wrapping the alphabet (after Z comes A) |
| `for` loop | Brute force — iterating all 25 shifts |
| DOM manipulation | `createElement()`, `appendChild()`, `classList` |
| Template literals | Backtick strings with `${}` variable embedding |
| Regular expressions | `/[A-Z]/`, `/[0-9]/` — detecting character types |
| CSS variables | `--gold`, `--bg` — consistent theming |

---

## Project Structure

```
cipherlab/
├── index.html    ← The entire application (HTML + CSS + JS in one file)
└── README.md     ← This file
```

---

## Roadmap

- [x] Caesar cipher (encrypt/decrypt)
- [x] Adjustable shift slider
- [x] Password strength analyzer (6-criteria scoring)
- [x] Common password blocklist
- [x] Brute force demo
- [ ] Shift position numbers displayed on cipher alphabet
- [ ] Entropy calculator (bits of entropy per password)
- [ ] Python CLI version of both tools

---

## Portfolio Context

This is **Project 01** in a progressive cybersecurity portfolio. Each project teaches programming concepts through a security lens.

Built by a software engineering student learning JavaScript and Python while building real security tools.

---

## License

For educational and portfolio use.

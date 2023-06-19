# (k, n) secret image-sharing scheme capable of cheating detection

A Python implementation of the paper *Liu, Y.-X., Sun, Q.-D., & Yang, C.-N. (2018). (k, n) secret image sharing scheme capable of cheating detection. EURASIP Journal on Wireless Communications and Networking, 2018(1), 72. doi:10.1186/s13638-018-1084-7*

## Main Structure 

```txt
.
├── src/
│   ├── __init__.py
│   ├── bmp_file.py
│   ├── constants.py
│   ├── distribute_image.py
│   ├── main.py
│   ├── polynomial.py
│   ├── recover_image.py
│   ├── utils.py
│   └── z251.py
└── test/
    ├── __init__.py
    ├── test_bmp_file.py
    ├── test_distribute_image.py
    ├── test_polynomial.py
    └── test_z251.py
```


## Running the program

For help

```bash
$ python3 -m src.main -h
usage: main.py [-h] {d,r} secret_image k directory

Distribute or recover secret images.

positional arguments:
  {d,r}         Operation to perform ('d' for distribute, 'r' for recover)
  secret_image  Name of the secret image file (.bmp)
  k             Minimum number of shadows to recover the secret in a (k, n) scheme
  directory     Directory containing the images (.bmp)

options:
  -h, --help    show this help message and exit
```

Example:

```bash
python3 -m src.main d images/secret.bmp 4 images/covers/
python3 -m src.main r images/secret.bmp 5 images/shares/ 
```

## Running tests

Run all the tests with:

```bash
python -m unittest
```

Run a specific test with:

```bash
python -m unittest test/test-file-you-want-to-test.py
```
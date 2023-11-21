# ft_otp

**ft_otp** encourages us **to implement a TOTP generator**. To use this generator you will have to clone the repository:

    git clone https://github.com/pgomez-a/ft_otp.git ; cd ./ft_otp/
    
Run make to compile the program:

    make
    
Use **-g hex_filename** to store and encrypt the key in hex_filename and store it in ft_otp.key:

    # hex_filename must have a hexadecimal number of at least 64 bits
    ./ft_otp -g hex_filename
    
Use **-k ft_otp.key** to create a TOTP with the secret key stored in ft_otp.key:

    ./ft_otp -k ft_otp.key

### 2-Factor Authentication (2FA)
**2FA** enhances the security of a system by adding an additional layer of security. When a user tries to access a system (such as a server or a service) they must **authenticate with a password and an additional token** that the user must have in order to access the system.<br>
Thus, with 2FA, there are two layers of security that the user must go through to access private data. Without that second token, a hacker cannot access the system even if the first password is known. One way to achieve this 2FA is through the use of **One-Time Passwords**, which will be described below.

### One-Time Passwords (OTP)
A **One Time Password (OTP)** is an automatically generated sequence of numeric or alphanumeric characters to authenticate users for a single sign-on. An OTP is a multi-factor authentication factor used to guarantee access to private data. The main characteristics of an OTP are the following:
- **It expires quickly.**
- **It can't be reused.**

One-time passwords are generated using a random code that is generated each time a new password request is made. There are three different ways that allow a user to obtain their OTP:
- An authentication token.
- A unique time-based password, also known as **TOTP**.
- A unique password based on HMAC, also known as **HOTP**.

### HMAC-based One-Time Passwords (HOTP)

> **HMAC:** A specific construct done to compute an **Authentication Message Code (MAC)** involving a cryptographic hash function combined with a secret key.

This type of OTP is event-based, which implies an **HMAC-based one-time password**. The HMAC algorithm needs two values to generate the key:
- **A secret key:** only known by the token and the server that validates the OTP codes.
- **A moving factor:** it is a counter stored on the server and in the token.

> **SHA1:** cryptographic hash function that provides a hash of 160 bits from any input value.

To obtain an OTP, the token provides the counter to the HMAC using the secret key. Additionally, the HMAC uses the **SHA-1 algorithm** to obtain a 160-bit string that is compressed to 6 digits.

### Time-based One-Time Passwords (TOTP)
**TOTP** is based on HTOP. Although this time **the moving factor is time** instead of a counter. TOTP uses time in 30 or 60 second increments, so the OTP will be valid during that time interval.<br>

To implement our TOTP algorithm we will follow **[RFC 6238](https://datatracker.ietf.org/doc/html/rfc6238#section-4.2).** This document describes the TOTP function as follows:

    # TOTP Function
    TOTP(secret_key) = HOTP(secret_key, counter)
    
    # TOTP parameters
    counter = (Current Unix time - T0) / X
    T0 = 0 (by default)
    Time Step X = 30 (by default)
    
So we see that TOTP implements HOTP, so now we focus on **[RFC 4226](https://datatracker.ietf.org/doc/html/rfc4226#section-5.3)**:

    # First Step: obtain 20-byte string with HMAC-SHA1
    HS = HMAC-SHA1(secret_key, counter)
    
    # Second Step: dynamic truncation (DT)
    Sbits = DT(HS)
    
    # Third Step: otain HOTP value
    HOTP value = Sbits mod 10^6

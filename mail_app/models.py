from dataclasses import dataclass


@dataclass
class Mail:
    to: str
    from_addr: str | None
    ea: str | None
    eb: str
    es: str


@dataclass
class Session:
    key: str
    iv: str


@dataclass
class EncryptedMail:
    mail: Mail
    session: Session
    # meta: Meta


# Create your models here.

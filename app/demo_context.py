from dataclasses import dataclass

from fastapi import HTTPException
from app.config import settings


@dataclass(frozen=True)
class Principal:
    tenant: str
    subject: str
    groups: list[str]
    admin: bool


def principal() -> Principal:
    """
    Return the shared demo identity.

    This is for single-workspace demonstration only.
    It does not authenticate or distinguish individual users.
    """
    s = settings()

    groups = [
        group.strip()
        for group in s.demo_groups.split(',')
        if group.strip()
    ]

    if not s.demo_tenant_id.strip() or not s.demo_subject.strip() or not groups:
        raise HTTPException(
            status_code=500,
            detail='Demo identity configuration is invalid.'
        )

    return Principal(
        tenant=s.demo_tenant_id.strip(),
        subject=s.demo_subject.strip(),
        groups=groups,
        admin=s.demo_admin,
    )

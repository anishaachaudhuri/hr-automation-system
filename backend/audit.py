from backend.db import SessionLocal

from backend.models import AuditLog


def create_audit_log(
    action_type,
    changed_field="",
    old_value="",
    new_value="",
    description=""
):

    db = SessionLocal()

    log = AuditLog(

        action_type=action_type,

        changed_field=changed_field,

        old_value=str(old_value),

        new_value=str(new_value),

        description=description
    )

    db.add(log)

    db.commit()

    db.close()
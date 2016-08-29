#!/usr/bin/env python
# encoding: utf-8

"""
This is the main 
"""

def historify(cls):
    """
    Create a new history table for the provided database model (``cls``),
    and wire up before_update and after_insert hooks on the class that will
    record any changes that occur. The history entries of the model can be
    found in a ``history`` backref on instances of the ``cls``.

    The history table is defined as:

        class XXXXHistory(db.Model):
            model_id       = db.Column(db.Integer, db.ForeignKey(table_name + ".id"), primary_key=True, index=True),
            model          = relationship(class_name, backref=backref("history", cascade="save-update, merge, delete, delete-orphan")),
            date           = db.Column(db.DateTime, default=datetime.datetime.utcnow),
            updated_by     = db.Column(db.String(100), nullable=False, default=get_current_username),
            changed_fields = db.Column(db.Text, nullable=False, default=""),
            
            def __repr__(self):
                return "<{} on {} by {} changed {}>".format(
                    history_name,
                    self.date,
                    self.updated_by,
                    self.changed_fields
                )

    Note that XXXX will be replaced with the provided cls' name.
    """

    table_name = cls.__tablename__
    class_name = cls.__name__

    history_name = class_name + "History"
    history_table = table_name + "_histories"

    new_cls = type(
        class_name + "History",   # name of the class
        (db.Model,),               # bases
        dict(                     # members
            __tablename__  = history_table,
            id             = db.Column(db.Integer, primary_key=True),
            model_id       = db.Column(db.Integer, db.ForeignKey(table_name + ".id"), primary_key=True, index=True),
            model          = relationship(class_name, backref=backref("history", cascade="save-update, merge, delete, delete-orphan")),
            date           = db.Column(db.DateTime, default=datetime.datetime.utcnow),
            updated_by     = db.Column(db.String(100), nullable=False, default=get_current_username),
            changed_fields = db.Column(db.Text, nullable=False, default=""),
            __repr__       = lambda self: "<{} on {} by {} changed {}>".format(
                history_name,
                self.date,
                self.updated_by,
                self.changed_fields
            )
        )
    )
    # so it will be accessible as XXXXHistory
    globals()[history_name] = new_cls

    sqlalchemy.event.listen(cls, "before_update", _handle_model_update_history)
    sqlalchemy.event.listen(cls, "after_insert", _handle_model_insert_history)

    return cls


def get_current_username():
    """Get the current username. Checks flask_login.current_user by default,
    optionally checking flask_jwt.current_identity (depending on configuration
    settings).
    """
    username = "<<manual>>"

    try:
        if not current_user.is_anonymous:
            username = current_user.username
        else:
            # TODO config setting for using flask_jwt
            username = flask_jwt.current_identity.username
    except:
        pass
    return username


def _get_changed_fields(model):
    """Get a dict of all of the changed columns in the model, with
    old and new values.
    """
    res = {}
    for k in model.__table__.columns._data.keys():
        v = getattr(model, k)
        if k.startswith("_sa_"):
            continue
        hist = get_history(model, k)
        if hist.has_changes():
            res[k] = {
                "from": str(hist.deleted),
                "to": str(hist.added)
            }
    return res


def _handle_model_update_history(mapper, connection, target):
    """Get list of changed columns in the target and create a new history
    record for the target.
    """
    history_class = globals()[target.__class__.__name__ + "History"]
    changed_fields = _get_changed_fields(target)

    if len(changed_fields) == 0:
        return
    if target.id is None:
        return

    insert = history_class.__table__.\
        insert().\
        values(
            model_id = target.id,
            changed_fields = json.dumps(changed_fields),
        )
    result = connection.execute(insert)


def _handle_model_insert_history(mapper, connection, target):
    """Simply note when and by whom the model was created
    """
    if target.id is None:
        return
    history_class = globals()[target.__class__.__name__ + "History"]
    insert = history_class.__table__.\
        insert().\
        values(
            model_id = target.id,
            changed_fields = "created",
        )
    result = connection.execute(insert)

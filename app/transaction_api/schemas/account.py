from marshmallow import Schema, fields


class AccountBase(Schema):
    id:Mapped[UUID]=mapped_column("account_id", UUID, default=uuid4, primary_key=True)
    id=fields.Str()
    user_id:Mapped[UUID]=mapped_column("user_id", UUID, ForeignKey("user.user_id"))
    
    account_type:Mapped[str]= mapped_column("account_type", String(50))
    account_number:Mapped[str]= mapped_column("account_number", String(50), unique=True)
    balance:Mapped[float]= mapped_column("balance",DECIMAL(10,2))
    
    created_at = mapped_column("created_at", DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column("updated_at",DateTime(timezone=True), onupdate=func.now())
    
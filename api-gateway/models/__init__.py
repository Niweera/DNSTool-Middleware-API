import json
from typing import List, Dict, Any
from marshmallow import Schema, fields, validates_schema, ValidationError
from marshmallow.fields import String, Email
from os.path import abspath, join, dirname, realpath


# Validation Schemas #######################
class UserSchema(Schema):
    full_name: String = fields.Str(required=True)
    email: Email = fields.Email(required=True)
    organization: String = fields.Str(required=True)
    profession: String = fields.Str(required=True)
    reason: String = fields.Str(required=True)
    password: String = fields.Str(required=True)

    @validates_schema
    def check_org_email(self, user_data: Dict[str, Any], **kwargs) -> None:
        email: str = user_data.get("email")
        domain: str = email.split("@")[1]
        levels: List[str] = domain.split(".")

        white_list_json: str = abspath(
            join(
                dirname(dirname(realpath(__file__))), "static", "whitelist-domains.json"
            )
        )
        with open(
            file=white_list_json, mode="r", encoding="utf-8"
        ) as white_list_json_file:
            white_list: List[str] = json.load(white_list_json_file)

        domain_is_accepted: bool = (
            len(
                list(
                    filter(
                        lambda exists: exists,
                        [
                            ".".join(levels[-i:]) in white_list
                            for i in range(2, len(levels) + 1)
                        ],
                    )
                )
            )
            > 0
        )

        if not domain_is_accepted:
            raise ValidationError(
                f"[{domain}] email domain is not an accepted organization domain."
            )

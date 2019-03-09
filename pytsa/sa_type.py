from pytsa._base_rule import new_rule

sa_type = new_rule(
    rule_name='sa_type',
    rule_types_name='type',
    rule_rules={},
    type_checker=lambda val: isinstance(val, type)
)

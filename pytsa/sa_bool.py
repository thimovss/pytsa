from pytsa._base_rule import new_rule

sa_bool = new_rule(
    rule_name='sa_bool',
    rule_types_name='bool',
    rule_rules={},
    type_checker=lambda val: isinstance(val, bool)
)

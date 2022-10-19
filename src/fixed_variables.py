class list_domains_filters:

    class status:
        active="active"
        inactive="inactive"

    class validation:
        # For more info: https://dev.digicert.com/services-api/domains/list-domains/#validation-filter-values
        completed="completed"
        ov_expired="ov_expired"
        ev_expired="ev_expired"
        ov_expiring="ov_expiring"
        ev_expiring="ev_expiring"
        ov_expired_in_last_7_days="ov_expired_in_last_7_days"
        ev_expired_in_last_7_days="ev_expired_in_last_7_days"
        ov_expiring_within_7_days="ov_expiring_within_7_days"
        ev_expiring_within_7_days="ev_expiring_within_7_days"
        ov_expiring_within_30_days="ov_expiring_within_30_days"
        ev_expiring_within_30_days="ev_expiring_within_30_days"
        ov_expiring_from_31_to_60_days="ov_expiring_from_31_to_60_days"
        ev_expiring_from_31_to_60_days="ev_expiring_from_31_to_60_days"
        ov_expiring_from_61_to_90_days="ov_expiring_from_61_to_90_days"
        ev_expiring_from_61_to_90_days="ev_expiring_from_61_to_90_days"

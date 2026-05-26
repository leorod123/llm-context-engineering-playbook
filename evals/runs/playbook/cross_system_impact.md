No, not as a purely local billing change. The refund_cross_system_contract says
refund behavior crosses billing, notifications, and scheduler. The refund worker
must not send customer emails directly, and retry scheduling must remain
idempotent. Review the contract and validation evidence before changing it.

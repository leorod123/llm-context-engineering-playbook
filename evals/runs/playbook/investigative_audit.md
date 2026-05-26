The duplicate-email issue is a hypothesis, not a confirmed cause. Start with
refund_pipeline_validation and refund_cross_system_contract. The audit should
separate billing refund emission from notifications delivery, look for contrary
evidence, record negative results, and avoid patching until evidence confirms
where duplication occurs.

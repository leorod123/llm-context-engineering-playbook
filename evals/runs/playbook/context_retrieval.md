Before changing refund retry behavior, use the registry/discovery output for
billing or refund_worker. The key docs are refund_pipeline_validation and
refund_cross_system_contract. Do not use raw/old_refund_notes as default
authority. The context is restricted and only partially validated, so the change
needs explicit limitations. Cross-system review is needed because notifications
and scheduler are downstream.

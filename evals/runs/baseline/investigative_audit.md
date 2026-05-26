The likely cause is that the refund worker sends duplicate email requests. I
would patch the worker to skip sending a second notification when a refund is
retried.

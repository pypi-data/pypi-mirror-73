from airflow.models import BaseOperator
from airflow_tm1.hooks.tm1 import TM1Hook

class TM1RunTIOperator(BaseOperator):
    """
    This operator runs a TI process

    :param ti_name: The TI process to run.
    :type ti_name: str
    :param tm1_conn_id: The Airflow connection used for TM1 credentials.
    :type tm1_conn_id: str
    """
    def __init__(self,
                 ti_name: str,
                 tm1_conn_id: str = "tm1_default",
                 **kwargs) -> None:
#        super().__init__(*args, **kwargs)
        self.ti_name = bucket_name
        self.tm1_conn_id = aws_conn_id

    def execute(self, context):
        tm1_hook = TM1Hook(tm1_conn_id=self.tm1_conn_id)
        if not tm1_hook.check_for_bucket(self.bucket_name):

                    return self.tm1.processes.execute_with_return(ti_name, **kwargs)
            s3_hook.create_bucket(bucket_name=self.bucket_name, region_name=self.region_name)
            self.log.info("Created bucket with name: %s", self.bucket_name)
        else:
            self.log.info("Bucket with name: %s already exists", self.bucket_name)


        return .processes.execute_with_return(ti_name, **kwargs)
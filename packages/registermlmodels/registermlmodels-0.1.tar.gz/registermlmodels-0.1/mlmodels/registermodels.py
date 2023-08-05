import mlflow
import mlflow.xgboost
import time
from mlflow.tracking.client import MlflowClient
from mlflow.entities.model_registry.model_version_status import ModelVersionStatus

def hello_world():
  print("Library is working fine. Hello World!!")

#### Provide parameters in this method as follows:
#### run_id = run_id
#### model_name = "dominos_cltv_xgb_alsea"
#### artifact_path = "dominos_cltv_xgb_alsea"
def get_model_details(run_id, model_name, artifact_path):
  model_name = model_name
  artifact_path = artifact_path
  model_uri = "runs:/{run_id}/{artifact_path}".format(run_id=run_id, artifact_path=artifact_path)
  model_details = mlflow.register_model(model_uri=model_uri, name=model_name)

  return model_details

#### Wait until the model is ready, Provide parameters to method as follows:
#### model_name = This will be returned by get_model_details method
#### model_version = This will be returned by get_model_details method
def wait_until_ready(model_name, model_version):
  client = MlflowClient()
  for _ in range(10):
    model_version_details = client.get_model_version(
      name=model_name,
      version=model_version,
    )
    status = ModelVersionStatus.from_string(model_version_details.status)
    print("Model status: %s" % ModelVersionStatus.to_string(status))
    if status == ModelVersionStatus.READY:
      break
    time.sleep(1)

##### Provide parameters to method as follows:
##### experiment_id = 179518594392967
##### model_name = "dominos_cltv_xgb_alsea"
##### model_path = "/dbfs/dominos_cltv_xgb_alsea/xgb-results.model"
##### xgb_instance = xgb
def start_ml_run(experiment_id, model_name, model_path, xgb_instance):
  mlflow.end_run()
  with mlflow.start_run(experiment_id=experiment_id) as active_run:
    deploy_uuid = active_run.info.run_id
    mlflow.xgboost.log_model(xgb_instance, model_name)
    #modelpath = "/dbfs/dominos_cltv_xgb_alsea/{}/xgb-results.model".format(deploy_uuid)
    mlflow.xgboost.save_model(xgb_instance, model_path)

  return active_run

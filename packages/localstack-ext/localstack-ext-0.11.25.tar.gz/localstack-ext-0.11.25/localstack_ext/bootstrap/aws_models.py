from localstack.utils.aws import aws_models
oVgPl=super
oVgPD=None
oVgPC=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  oVgPl(LambdaLayer,self).__init__(arn)
  self.cwd=oVgPD
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,oVgPC,env=oVgPD):
  oVgPl(RDSDatabase,self).__init__(oVgPC,env=env)
 def name(self):
  return self.oVgPC.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,oVgPC,env=oVgPD):
  oVgPl(RDSCluster,self).__init__(oVgPC,env=env)
 def name(self):
  return self.oVgPC.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)

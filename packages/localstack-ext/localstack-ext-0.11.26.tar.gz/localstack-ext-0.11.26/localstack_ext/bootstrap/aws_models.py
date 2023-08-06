from localstack.utils.aws import aws_models
EohRp=super
EohRK=None
EohRQ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  EohRp(LambdaLayer,self).__init__(arn)
  self.cwd=EohRK
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,EohRQ,env=EohRK):
  EohRp(RDSDatabase,self).__init__(EohRQ,env=env)
 def name(self):
  return self.EohRQ.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,EohRQ,env=EohRK):
  EohRp(RDSCluster,self).__init__(EohRQ,env=env)
 def name(self):
  return self.EohRQ.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)

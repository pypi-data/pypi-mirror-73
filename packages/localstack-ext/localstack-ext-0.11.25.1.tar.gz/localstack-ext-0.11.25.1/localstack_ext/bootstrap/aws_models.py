from localstack.utils.aws import aws_models
yKvPe=super
yKvPM=None
yKvPQ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  yKvPe(LambdaLayer,self).__init__(arn)
  self.cwd=yKvPM
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,yKvPQ,env=yKvPM):
  yKvPe(RDSDatabase,self).__init__(yKvPQ,env=env)
 def name(self):
  return self.yKvPQ.split(':')[-1]
class RDSCluster(aws_models.Component):
 def __init__(self,yKvPQ,env=yKvPM):
  yKvPe(RDSCluster,self).__init__(yKvPQ,env=env)
 def name(self):
  return self.yKvPQ.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)

import yaml, os
from typing import List

def env_entries(keys:List[str], env_defs:dict):
        for key in keys:
            entry = env_defs[key]
            yield f'{key}={entry}'


class FunctionDefinition:
    def __init__(self, name:str, source:str, env:List[str], runtime:str,
            s3_bucket:str, aws_region:str, aws_profile:str
        ):
        self.name = name
        self.source = source
        self.runtime = runtime

        self.environments = env
        self.s3_bucket = s3_bucket
        self.aws_region = aws_region
        self.aws_profile = aws_profile
    
    @property
    def create_command(self) -> str:
        return f'''
            aws lambda create-function 
                --function-name {self.name} 
                --runtime {self.runtime}
                --handler main
                --environment {self.environments}
                --code
                --S3Bucket={self.s3_bucket}
                --S3Key={self.source}
                --timeout 200
                --region {self.aws_region}
                --profile {self.aws_profile}
        '''

    @property
    def update_command(self) -> str:
        return f'''
            aws lambda update-function-code
                --function-name {self.name}
                --s3-bucket {self.s3_bucket}
                --s3-key {self.source}
                --region {self.aws_region}
                --profile {self.aws_profile}
        '''

    # def __str__(self) -> str:
    #     pass
 
class Config:
    def __init__(self, config:dict):
        env_definitions = config['environments']['definition']
        global_env_keys = config['environments']['global-env']
        self._aws_config = config['aws-config']

        global_env = list(env_entries(global_env_keys, env_definitions))

        self.s3_bucket = self._aws_config['s3-bucket']
        self.aws_region = self._aws_config['region']
        self.aws_profile = self._aws_config['profile']

        functions = config['functions']
        runtime = functions['runtime']
        fn_devs = functions['definition']
        fndev_pairs = zip(fn_devs.keys(), fn_devs.values())

        self._function_definitions:List[FunctionDefinition] = []
        
        for key, entry in fndev_pairs:
            envs = global_env
            if 'local-env' in entry:
                envs = envs + list(env_entries(entry['local-env'], env_definitions ) )

            self._function_definitions.append(
                FunctionDefinition(
                    name=key, source=entry['source'],
                    env=envs, runtime=runtime, 
                    s3_bucket=self.s3_bucket,
                    aws_region=self.aws_region,
                    aws_profile=self.aws_profile
                )
            )
    @property
    def function_definitions(self) -> List[FunctionDefinition]:
        return self._function_definitions
            

class ConfigParser:
    @classmethod
    def parse(cls, path:str, org:str):
        abspath = os.path.abspath(path)
        config_str = yaml.safe_load(open( os.path.join(abspath,f'config.{org}.yml')).read())
        return Config(config=config_str)


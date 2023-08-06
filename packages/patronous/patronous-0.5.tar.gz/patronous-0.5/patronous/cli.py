import yaml, sys, os
from glob import glob
import click
from pprint import pprint
from .utils import ConfigParser
from bash import bash
import logging
logging.basicConfig(level='INFO')


@click.group()
@click.argument('org')
@click.option('-p','--path', type=click.Path(), default='.')
@click.option('-v','--verbose',is_flag=True)
@click.option('-d','--dry-run',is_flag=True)
@click.pass_context
def cli(ctx, org=None, path='.', verbose='True', dry_run=True):
    ctx.ensure_object(dict)

    def gen_context():
        for f in glob('config.*.yml'):
            yield f.split('.')[1]

    contexes = [c for c in gen_context()]

    if org not in contexes:
        raise Exception(f"not recognized org, select from : {','.join(contexes)}")
    abspath = os.path.abspath(path)
    try:
        config = yaml.safe_load(open( os.path.join(abspath,f'config.{org}.yml')).read())
        ctx.obj = config
        ctx.obj['verbose'] = verbose
        ctx.obj['dry-run'] = dry_run
    except Exception as e:
        print(e)
        exit(1)
    
    # pprint(config)
    # print('path:', os.path.abspath(path)  )
    
    

@cli.command()
@click.pass_context
def update(ctx):
    env_defs = ctx.obj['environments']['definition']
    genv_keys = ctx.obj['environments']['global-env']
    aws_config = ctx.obj['aws-config']

    s3_bucket = aws_config['s3-bucket']
    aws_region = aws_config['region']
    aws_profile = aws_config['profile']
    for fn_key in ctx.obj['functions']:
        fn_def = ctx.obj['functions'][fn_key]
        cmd = f"aws lambda update-function-code --function-name {fn_key} --s3-bucket {s3_bucket} --s3-key {fn_def['source']} --region {aws_region} --profile {aws_profile} "
        if ctx.obj['verbose']:
            click.echo(cmd)
        if not ctx.obj['dry-run']:
            pass
            #fuking run it!
@cli.command()
@click.pass_context
def patronum(ctx):
    click.echo("up!")

    def env_entries(keys, env_defs):
        for key in keys:
            entry = env_defs[key]
            yield f'{key}={entry}'

    envs = ctx.obj['environments']
    aws_config = ctx.obj['aws-config']
    env_defs = envs['definition']
    genv_keys = envs['global-env']
    # genv = [f'{key}={entry}' for key, entry in zip(genv_keys, [ env_defs[key] for key in genv_keys])]
    # genv = [f'{key}={entry}' for key, entry in zip(genv_keys, [entry for entry in genv_entries(genv_keys, env_defs)])]
    genv = list(env_entries(genv_keys, env_defs))
    s3_bucket = aws_config['s3-bucket']
    aws_region = aws_config['region']
    aws_profile = aws_config['profile']
    runtime = ctx.obj['functions']['runtime']
    aws_role = aws_config['role']
    fn_defs = ctx.obj['functions']['definition']
    verbose = ctx.obj['verbose']
    dry_run = ctx.obj['dry-run']

    for fn_key, fn_def in zip(fn_defs.keys(), fn_defs.values()):
        # fn_def = fn_defs[fn_key]
        lenv = []
        if 'local-env' in fn_def:
            lenv_keys = fn_def['local-env']
            # lenv = [f'{key}={entry}' for key, entry in zip(lenv_keys, [env_defs[key] for key in lenv_keys])]
            lenv = list(env_entries(lenv_keys, env_defs))

        env_vars = f'Variables={{{",".join(genv+lenv)}}}'
        
        cmd = f"""aws lambda create-function --function-name {fn_key} 
                --runtime {runtime} 
                --role {aws_role} 
                --handler main 
                --environment {env_vars} 
                --code
                --S3Bucket={s3_bucket} 
                --S3Key={fn_def['source']} 
                --timeout 200
                --region {aws_region} 
                --profile {aws_profile} """

        if verbose:
            click.echo(cmd)

        if not dry_run:
            pass
            #fuking run it!

        click.echo("running command")

def main():
    cli(obj={})

@click.command()
@click.option('-l','--locatio', type=click.Path(), default='.')
@click.option('-u','--unafecta', default=False , is_flag=True)
@click.argument("org")
def lumos(org, locatio, unafecta:bool):
    cfg = ConfigParser.parse(org=org, path=locatio)
    log = logging.getLogger()

    fn_defs = cfg.function_definitions
    for fn_def in fn_defs:
        cstmt = fn_def.update_command
        if not unafecta:
            pass
            log.info("running is deactivated")
            # b = bash(cstmt)
            # b.stdout
            # b.stderr
        else:
            log.info(f"dry run {cstmt}")

@click.command()
@click.option('-l','--locatio', type=click.Path(), default='.')
@click.option('-u','--unafecta', default=False , is_flag=True)
@click.argument("nox")
def nox(org, locatio, unafecta:bool):
    pass
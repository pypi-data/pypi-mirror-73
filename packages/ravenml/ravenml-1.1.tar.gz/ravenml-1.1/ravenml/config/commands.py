"""
Author(s):      Carson Schubert (carson.schubert14@gmail.com)  
Date Created:   04/05/2019

Command group for setting ravenml configuration.
"""

import click
from pathlib import Path
from colorama import Fore
from ravenml.utils.question import user_input, user_confirms
from ravenml.utils.config import CONFIG_FIELDS, get_config, update_config

### OPTIONS ###
image_bucket_name_opt = click.option(
    '-i', '--image-bucket', type=str, is_eager=True,
    help='Image bucket name.')
    
dataset_bucket_name_opt = click.option(
    '-d', '--dataset-bucket', type=str, is_eager=True,
    help='Dataset bucket name.')

model_bucket_name_opt = click.option(
    '-m', '--model-bucket', type=str, is_eager=True,
    help='Model artifact destination bucket name.')


### COMMANDS ###
@click.group(help='Configuration commands.')
@click.pass_context
def config(ctx: click.Context):
    """Configuration command group.

    Args:
        ctx (Context): click context object
    """
    ctx.obj = {}
    ctx.obj['from_show'] = False     # flag to indicate if entering update from show

@config.command(help='Show current config.')
@click.pass_context
def show(ctx: click.Context):
    """Show current config.
    
    Args:
        ctx (Context): click context object
    """
    try:
        # try and load the configuration
        config = get_config()
        for key, value in config.items():
            print(Fore.GREEN + key + ': ' + Fore.WHITE + value)
    except FileNotFoundError:
        # thrown when no configuration file is found
        click.echo(Fore.RED + 'No configuration found.')
        if user_confirms('Would you like to make a new configuration?', default=True):
            ctx.obj['from_show'] = True
            ctx.invoke(update)
    except ValueError:
        # thrown when current configuration file is invalid
        click.echo(Fore.RED + 'Current configuration file is invalid.')
        if user_confirms('Would you like to fix it?', default=True):
            ctx.obj['from_show'] = True
            ctx.invoke(update)

@config.command(help='Update current config.')
@click.pass_context
@model_bucket_name_opt
@dataset_bucket_name_opt
@image_bucket_name_opt
def update(ctx: click.Context, image_bucket: str, dataset_bucket: str, model_bucket: str):
    """Update current config.
    
    Args:
        ctx (Context): click context object
        artifact_bucket (str): artifact bucket name. None if not in no-user mode
        dataset_bucket (str): dataset bucket name. None if not in no-user mode
    """
    config = {}
    load_result = 0
    try: 
        # try and load the configuration
        config = get_config()
    except FileNotFoundError:
        # thrown when no configuration file is found
        # checks to see if flag is set to indicate we arrived here from show
        if not ctx.obj['from_show']:
            click.echo(Fore.RED + 'No configuration found to update. A new one will be created.')
        load_result = 1
    except ValueError:
        # thrown current configuration file is invalid
        # checks to see if flag is set to indicate we arrived here from show
        if not ctx.obj['from_show']:
            click.echo(Fore.RED + 'Current configuration is invalid. A new one will be created.')
        load_result = 2

    # map options into dict
    user_options = {
        'image_bucket_name': image_bucket,
        'dataset_bucket_name': dataset_bucket,
        'model_bucket_name': model_bucket,
    }
    
    # if options were passed, just update those options
    if (image_bucket or dataset_bucket or model_bucket):
        # only use options if existing config was valid or a new config is beig created
        if load_result == 0 or load_result == 1:
            for field, value in user_options.items():
                if value:
                    config[field] = value
        else:
            click.echo(Fore.RED + "Passed options ignored since current configuration is invalid.")
    # otherwise iterate over each field
    else:
        for field in CONFIG_FIELDS:
            # only make field editing optional if existing config was loaded successfully
            if load_result == 0:
                if user_confirms('Edit ' + field + '?'):
                    config[field] = user_input(field + ':', default=config[field]) 
            else:
                config[field] = user_input(field + ':')

    # save updates
    update_config(config)

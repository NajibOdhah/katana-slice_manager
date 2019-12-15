import requests
import json
import click


@click.group()
def cli():
    """Manage General Slice Template"""
    pass


@click.command()
def ls():
    """
    List all resources
    """
    url = "http://localhost:8000/api/resources"
    r = None
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        json_data = json.loads(r.content)
        click.echo(json.dumps(json_data, indent=2))
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)


@click.command()
@click.argument('location')
def location(location):
    """
    List all resources in the specific location
    """
    url = "http://localhost:8000/api/resources/"+location
    r = None
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        json_data = json.loads(r.content)
        click.echo(json.dumps(json_data, indent=2))
        if not json_data:
            click.echo("Error: No such GST: {}".format(id))
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)


cli.add_command(ls)
cli.add_command(location)
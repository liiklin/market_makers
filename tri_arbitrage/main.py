import click
import json
@click.option("--config", 
    type=str, 
    help="Json config file", 
    default="app_config.json")
@click.pass_context
def main(ctx, **kwargs):
    ctx.obj = {}
    for k, v in kwargs.items():
        ctx.obj[k] = v
    if "config" in ctx.obj:
        #Read JSON data into the datastore variable
        with open(ctx.obj["config"], 'r') as f:
            datastore = json.load(f)
            for k, v in datastore:
                ctx.obj[k] = v
    print "context %s"  % (ctx.obj)

if __name__ == "__main__":
    main()
"""Parse Terraform Plan file."""


def parse_json(filename=None):
    """Parse Terraform plan in json format.

    To create the plan in json format you can use
    `terraform show -no-color plan.out > plan.json`
    """
    print("Filename %s" % filename)

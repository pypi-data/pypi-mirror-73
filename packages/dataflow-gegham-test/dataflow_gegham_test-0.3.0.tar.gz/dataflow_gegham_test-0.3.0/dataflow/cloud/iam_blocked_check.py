from typing import Dict, List, Optional

import boto3


def blocked(
    actions: List[str],
    resources: Optional[List[str]] = None,
    context: Optional[Dict[str, List]] = None,
) -> List[str]:
    """test whether IAM user is able to use specified AWS action(s)

    Args:
        actions (list): AWS action(s) to validate IAM user can use.
        resources (list): Check if action(s) can be used on resource(s).
            If None, action(s) must be usable on all resources ("*").
        context (dict): Check if action(s) can be used with context(s).
            If None, it is expected that no context restrictions were set.

    Returns:
        list: Actions denied by IAM due to insufficient permissions.
    """
    if not actions:
        return []
    actions = list(set(actions))

    if resources is None:
        resources = ["*"]

    _context: List[Dict] = [{}]
    if context is not None:
        # Convert context dict to list[dict] expected by ContextEntries.
        _context = [
            {
                "ContextKeyName": context_key,
                "ContextKeyValues": [str(val) for val in context_values],
                "ContextKeyType": "string",
            }
            for context_key, context_values in context.items()
        ]

    # You'll need to create an IAM client here
    user = boto3.client("sts").get_caller_identity()
    arn = user.get("Arn")
    client = boto3.client("iam")
    results = client.simulate_principal_policy(
        PolicySourceArn=arn,  # "arn:aws:iam::147777122203:user/edward",  # Your IAM user's ARN goes here
        ActionNames=actions,
        ResourceArns=resources,
        ContextEntries=_context,
    )["EvaluationResults"]

    return sorted(
        [
            result["EvalActionName"]
            for result in results
            if result["EvalDecision"] != "allowed"
        ]
    )


def check_arns():
    """
        Checks if the user with environment credentials has access to required resources
    """
    missing_arns = blocked(
        [
            "ec2:AuthorizeSecurityGroupIngress",
            "ec2:CreateSecurityGroup",
            "ec2:CreateTags",
            "ec2:DescribeNetworkInterfaces",
            "ec2:DescribeSubnets",
            "ec2:DescribeVpcs",
            "ec2:DeleteSecurityGroup",
            "ecs:CreateCluster",
            "ecs:DescribeTasks",
            "ecs:ListAccountSettings",
            "ecs:RegisterTaskDefinition",
            "ecs:RunTask",
            "ecs:StopTask",
            "ecs:ListClusters",
            "ecs:DescribeClusters",
            "ecs:DeleteCluster",
            "ecs:ListTaskDefinitions",
            "ecs:DescribeTaskDefinition",
            "ecs:DeregisterTaskDefinition",
            "iam:AttachRolePolicy",
            "iam:CreateRole",
            "iam:TagRole",
            "iam:PassRole",
            "iam:DeleteRole",
            "iam:ListRoleTags",
            "iam:ListAttachedRolePolicies",
            "iam:DetachRolePolicy",
            "logs:DescribeLogGroups",
        ]
    )
    if len(missing_arns):
        raise Exception(
            f"Your AWS account is missing following arns: {str(missing_arns)}, please contact your administrator to access resources."
        )
    return None

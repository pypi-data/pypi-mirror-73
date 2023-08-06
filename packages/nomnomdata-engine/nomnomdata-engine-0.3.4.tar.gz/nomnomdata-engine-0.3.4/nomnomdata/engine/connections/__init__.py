from nomnomdata.engine.components import Connection, Parameter, ParameterGroup
from nomnomdata.engine.parameters import Enum, Int, String, Text

AWSTokenConnection = Connection(
    connection_type_uuid="AWS5D-TO99M",
    description="AWS Access Key Information.",
    alias="AWS:Token",
    categories=["aws", "access", "credentials"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                type=String(),
                name="aws_access_key_id",
                display_name="Access Key ID",
                description="First part of the Access Key.",
                required=True,
            ),
            Parameter(
                type=String(),
                name="aws_secret_access_key",
                display_name="Secret Access Key",
                description="Second part of the Access Key.",
                required=True,
            ),
            Parameter(
                type=String(),
                name="region",
                display_name="Region",
                description="Specify the AWS region that the session will be created within.",
                required=True,
            ),
            name="secret_info",
            display_name="Secret Info",
        ),
    ],
)

AWSS3BucketConnection = Connection(
    connection_type_uuid="AWSS3-BKH32",
    alias="AWS:S3:Bucket+Token",
    description="AWS Bucket Name and connection credentials.",
    categories=["aws", "bucket", "storage"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                type=String(),
                name="bucket",
                display_name="Bucket",
                description="Name of the Bucket",
                required=True,
            ),
            Parameter(
                type=String(),
                name="endpoint_url",
                display_name="S3 Endpoint URL",
                description="S3 Endpoint url for non-AWS hosted buckets.",
            ),
            Parameter(
                type=String(),
                name="prefix",
                display_name="Folder Path Prefix",
                description="Path prefix to apply towards any requests to this bucket.",
            ),
            Parameter(
                type=String(),
                name="s3_temp_space",
                display_name="S3 Temporary Path",
                description="Folder in which Tasks using this Connection may create temporary files. A folder named temp in the root of the bucket will be used if left blank.",
            ),
            name="bucket_info",
            display_name="Bucket Info",
        ),
        ParameterGroup(
            Parameter(
                type=String(),
                name="access_key_id",
                display_name="Access Key ID",
                description="First part of the Access Key.",
                required=True,
            ),
            Parameter(
                type=String(),
                name="secret_access_key",
                display_name="Secret Access Key",
                description="Second part of the Access Key.",
                required=True,
            ),
            name="secret_info",
            display_name="Secret Info",
        ),
    ],
)

FTPConnection = Connection(
    alias="FTP",
    description="FTP, FTPS or SFTP configuration.",
    connection_type_uuid="FTP92-TS0BZ",
    categories=["ftp", "sftp", "ftps"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="type",
                display_name="FTP Type",
                description="Type of FTP authentication to use",
                type=Enum(choices=["FTP", "FTPS Explicit", "SFTP"]),
                required=True,
            ),
            name="authentication_parameters",
            display_name="Authentication Parameters",
        ),
        ParameterGroup(
            Parameter(
                name="host_name",
                display_name="Hostname",
                description="DNS Host name of the server.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="port",
                display_name="FTP Port",
                description="Port 21 is the typical port for FTP and explicitly negotiated FTPS. Port 22 is the typical port for SFTP.",
                type=Int(min=1, max=65535),
                required=True,
                default=21,
            ),
            Parameter(
                name="username", display_name="Username", type=String(), required=False,
            ),
            Parameter(
                name="password", display_name="Password", type=String(), required=False,
            ),
            Parameter(
                name="ssh_key",
                display_name="SSH Private Key",
                description="This field is only used for key based SFTP authentication.",
                type=String(),
                required=False,
            ),
            name="server_parameters",
            description="Server Parameters",
        ),
    ],
)

GenericDatabaseConnection = Connection(
    alias="Generic:Database",
    description="Basic database access information.",
    connection_type_uuid="GNC8L-BG2T3",
    categories=["generic", "database"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="hostname",
                display_name="Hostname",
                description="DNS name used to connect to the database server or endpoint.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="port",
                display_name="Port",
                description="TCP Port used to connect. Port 3306 is the typical port for MySQL.",
                type=Int(min=1, max=65535),
                required=True,
                default=3306,
            ),
            Parameter(
                name="database",
                display_name="Database Name",
                description="Name of the database to connect to.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="db_engine",
                display_name="Database Type",
                description="Type of database to connect to.",
                type=Enum(choices=["mysql", "postgres"]),
                required=True,
                default="mysql",
            ),
            Parameter(
                name="username", display_name="Username", type=String(), required=False,
            ),
            Parameter(
                name="password", display_name="Password", type=String(), required=False,
            ),
            name="db_parameters",
            description="Database Parameters",
        ),
    ],
)

RedshiftDatabaseConnection = Connection(
    alias="Redshift Database",
    description="Redshift database access information.",
    connection_type_uuid="AWSDB-RSCON",
    categories=["AWS", "redshift", "database"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="hostname",
                display_name="Hostname",
                description="DNS name used to connect to the cluster endpoint.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="port",
                display_name="Port",
                description="TCP Port used to connect. Port 5439 is the typical port for Redshift clusters.",
                type=Int(min=1150, max=65535),
                required=True,
                default=5439,
            ),
            Parameter(
                name="database",
                display_name="Database Name",
                description="Name of the database to connect to within the cluster.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="db_engine",
                display_name="Database Type",
                description="Don't change this field value.",
                type=String(),
                required=True,
                default="redshift",
            ),
            Parameter(
                name="username", display_name="Username", type=String(), required=False,
            ),
            Parameter(
                name="password", display_name="Password", type=String(), required=False,
            ),
            name="db_parameters",
            description="Database Parameters",
        ),
    ],
)

SlackAPIConnection = Connection(
    alias="Slack:API:Token",
    description="Slack API token.",
    connection_type_uuid="SLKTK-O2B8D",
    categories=["API", "Slack"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="token",
                display_name="Token",
                description="Token string used to connect to Slack REST API's.",
                type=String(),
                required=True,
            ),
            name="slack_parameters",
            description="Slack Parameters",
        ),
    ],
)

SSHPrivateKeyConnection = Connection(
    alias="SSH Private Key",
    description="Private Key for SSH Authentication and Encryption.",
    connection_type_uuid="PVKEY-SSH01",
    categories=["SSH", "RSA", "Key"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="ssh_key",
                display_name="SSH Private Key",
                description="Private key string.",
                type=Text(),
                required=True,
            ),
            name="authentication_parameters",
            description="Authentication Parameters",
        ),
    ],
)

SSHHostConnection = Connection(
    alias="SSH Host",
    description="Remote Server SSH Session.",
    connection_type_uuid="SSH01-HOST1",
    categories=["SSH", "Secure", "Shell"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="hostname",
                display_name="Hostname",
                description="DNS name of the host machine.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="port",
                display_name="Port",
                description="TCP Port used for the secure shell connection. Port 22 is the typical port for SSH.",
                type=Int(min=1, max=65535),
                required=True,
                default=22,
            ),
            Parameter(
                name="username", display_name="Username", type=String(), required=True,
            ),
            Parameter(
                name="password",
                display_name="Password",
                description="Optional.  Used for password based authentication.",
                type=String(),
                required=False,
            ),
            Parameter(
                name="connect_timeout",
                display_name="TCP Connection Timeout",
                description="Optional.  Amount of seconds to wait for a successful TCP connection.",
                type=Int(),
                required=False,
            ),
            Parameter(
                name="private_key",
                display_name="Private Key",
                description="Optional.  Used for private key authentication and encryption.",
                type=Text(),
                required=False,
            ),
            name="server_parameters",
            description="Server Parameters",
        ),
    ],
)

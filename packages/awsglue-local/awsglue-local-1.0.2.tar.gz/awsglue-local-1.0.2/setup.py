# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awsglue', 'awsglue.transforms']

package_data = \
{'': ['*']}

install_requires = \
['pyspark>=2.2,<3.0']

setup_kwargs = {
    'name': 'awsglue-local',
    'version': '1.0.2',
    'description': 'Build Python interfaces to the AWS Glue ETL library for use as a local dependency.',
    'long_description': "# awsglue\n\nThe awsglue Python package contains the Python portion of the [AWS Glue](https://aws.amazon.com/glue) library. This library extends [PySpark](http://spark.apache.org/docs/2.1.0/api/python/pyspark.html) to support serverless ETL on AWS.\n\nNote that this package must be used in conjunction with the AWS Glue service and is not executable independently. Many of the classes and methods use the Py4J library to interface with code that is available on the Glue platform. This repository can be used as a reference and aid for writing Glue scripts.\n\nWhile scripts using this library can only be run on the AWS Glue service, it is possible to import this library locally. This may be helpful to provide auto-completion in an IDE, for instance. To import the library successfully you will need to install PySpark, which can be done using pip:\n\n      pip install pyspark\n\n## Content\n\nThis package contains Python interfaces to the key data structures and methods used in AWS Glue. The following are some important modules. More information can be found in the public documentation.\n\n\n#### GlueContext\nThe file [context.py](context.py) contains the GlueContext class. GlueContext extends PySpark's [SQLContext](https://github.com/apache/spark/blob/master/python/pyspark/sql/context.py) class to provide Glue-specific operations. Most Glue programs will start by instantiating a GlueContext and using it to construct a DynamicFrame. \n\n\n#### DynamicFrame\nThe DynamicFrame, defined in [dynamicframe.py](dynamicframe.py), is the core data structure used in Glue scripts. DynamicFrames are similar to Spark SQL's [DataFrames](https://github.com/apache/spark/blob/master/python/pyspark/sql/dataframe.py) in that they represent distributed collections of data records, but DynamicFrames provide more flexible handling of data sets with inconsistent schemas. By representing records in a self-describing way, they can be used without specifying a schema up front or requiring a costly schema inference step. \n\nDynamicFrames support many operations, but it is also possible to convert them to DataFrames using the `toDF` method to make use of existing Spark SQL operations. \n\n\n#### Transforms\n\nThe [transforms](transforms/) directory contains a variety of operations that can be performed on DynamicFrames. These include simple operations, such as `DropFields`, as well as more complex transformations like `Relationalize`, which flattens a nested data set into a collection of tables that can be loaded into a Relational Database. Once imported, transforms can be invoked using the following syntax:\n\n        TransformClass.apply(args...)\n\n## Additional Resources \n\n- The [aws-glue-samples](https://github.com/awslabs/aws-glue-samples) repository contains sample scripts that make use of awsglue library and can be submitted directly to the AWS Glue service.\n\n- The public [Glue Documentation](http://docs.aws.amazon.com/glue/latest/dg/index.html) contains information about the AWS Glue service as well as addditional information about the Python library.\n\n",
    'author': 'Ryan Eloff',
    'author_email': 'ryan.peter.eloff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rpeloff/aws-glue-libs/tree/glue-1.0',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3,<3.8',
}


setup(**setup_kwargs)

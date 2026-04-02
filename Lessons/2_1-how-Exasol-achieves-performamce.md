## Hardware Setup

Exasol Personal runs on AWS EC2 instances. The hardware setup determines cluster capacity and performance.

![Hardware Setup](../Script_Images/2_1/Hardware-setup.png)

## Distribution key

Manages where the data will be distributed -> enables horizontal scaling, quick writes and reads

![Distribution Key](../Script_Images/2_1/Distribution-key.png)

## Partition key

Creates logical partitions that reduce the amount of data needing to be "scanned" when running queries

![Partitioning Key](../Script_Images/2_1/Partitioning-key.png)

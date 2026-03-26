# Setup AWS User and Policies

## Step 1: Create IAM User for Exasol Personal

1. Sign in to the AWS Console
2. Navigate to IAM (Identity and Access Management)
3. Create a new IAM user for Exasol Personal
4. Attach the required policies to the user
5. Generate access keys (Access Key ID and Secret Access Key)

**Reference:** [Exasol Personal AWS Setup Guide](https://docs.exasol.com/db/latest/get_started/exasol_personal_aws_setup.htm)

## Step 2: Install and Configure AWS CLI

1. Install the AWS CLI following the [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
2. Verify the installation by running:
   ```bash
   aws --version
   ```
3. Configure the AWS CLI with the IAM user credentials:
   ```bash
   aws configure --profile exasol
   ```
4. When prompted, enter:
   - AWS Access Key ID (from Step 1)
   - AWS Secret Access Key (from Step 1)
   - Default region (e.g., us-east-1)
   - Default output format (optional)

5. Verify the configuration:
   ```bash
   aws sts get-caller-identity --profile exasol
   ```

## Step 3: Install Exasol Personal on AWS

1. Download the Exasol Launcher:
   ```bash
   curl https://downloads.exasol.com/exasol-personal/installer.sh | sh
   ```
   Alternatively, download from the [Exasol Download Portal](https://downloads.exasol.com) and add the `exasol` binary to your PATH.

2. Add the `exasol` binary to your PATH:
   ```bash
   export PATH="$PATH:/Users/<your-user>/<your-exasol-installer-directory>"
   ```
   To make this permanent, add the line to your shell profile (`~/.bash_profile` for bash or `~/.zshrc` for zsh).

3. Create and navigate to a deployment directory:
   ```bash
   mkdir deployment
   cd deployment
   ```

3. Set the AWS profile:
   ```bash
   export AWS_PROFILE=exasol
   ```

4. Run the installation:
   ```bash
   exasol install aws
   ```
   This generates Terraform files, provisions AWS infrastructure, and installs Exasol Personal. By default, it launches an **r6i.xlarge** instance. The process typically takes 10-20 minutes.

5. (Optional) Customize cluster size or instance type:
   ```bash
   exasol install aws --cluster-size <number> --instance-type <string>
   ```

6. View connection details:
   ```bash
   exasol info
   ```

**Reference:** [Exasol Quick Start Guide](https://docs.exasol.com/db/latest/get_started/quick_start_guide.htm)


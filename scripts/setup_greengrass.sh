#!/bin/bash

# Greengrass initial installation
mkdir ~/gg-setup && pushd ~/gg-setup
curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip
unzip greengrass-nucleus-latest.zip -d GreengrassInstaller && rm greengrass-nucleus-latest.zip
popd

sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE \
  -jar ./lib/Greengrass.jar \
  --aws-region us-west-2 \
  --thing-name GreengrassROS2Core \
  --thing-group-name GreengrassROS2CoreGroup \
  --thing-policy-name GreengrassV2IoTThingPolicy \
  --tes-role-name GreengrassV2TokenExchangeRole \
  --tes-role-alias-name GreengrassCoreTokenExchangeRoleAlias \
  --component-default-user ggc_user:ggc_group \
  --provision true \
  --deploy-dev-tools true \
  --setup-system-service true

# Update deployment with extra components
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
TARGET_ARN=$(aws iot describe-thing --thing-name GreengrassROS2Core --output text --query thingArn)
aws greengrassv2 create-deployment --target-arn $TARGET_ARN --components "file://$SCRIPT_DIR/greengrass_deployment_config.json"

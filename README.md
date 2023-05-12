# Setup

1) setup virual env - python3 -m venv .venv    
2) activate - source .venv/bin/activate
3) install dependencies - pip3 install -r requirements.txt
4) start application - python3 application.py



<!-- https://stackoverflow.com/questions/66627441/error-could-not-locate-a-flask-application -->
.flask env is there because we have application.py instead of app.py because its easier for deployment above like give more details
.db.py is there so db can be exported to the models and other places


This is how you convert glb to jsx: https://www.youtube.com/watch?v=xy_tbV4pC54 using package: https://www.npmjs.com/package/gltfjsx command: npx gltfjsx ./weapon.glb --transform


Infra setup:

Backend deployed via codepipeline to elastic beanstalk which is a ec2 container. the load balancer on that ec2 container has the certificates and Route53 maps to the loadbalancer url via a hosted zone with A Type record.


Front end is deployed via Amplify and is hosted via amplify aswell and it has the domain mapping for with certificate within amplify.





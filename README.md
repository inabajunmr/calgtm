# calgtm

## Build
### Prepare for first build
```
docker build -t mylambda .
```
### Build command
```
docker run -v "$PWD":/var/task mylambda
```
This command create deploy_package.zip.

## Deploy
### AWS Lambda
Upload deploy_package.zip to AWS Lambda.

### API Gateway
Lambda ploxy integration and specify binary media type.

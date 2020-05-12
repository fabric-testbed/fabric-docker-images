# AuthzForce RESTful PDP

## Versions Available

- [3.0.0](3.0.0/README.md)

## What is this?

[AuthzForce RESTful PDP](https://github.com/authzforce/restful-pdp) is a Spring-based REST server implementation of an XACML single-policy PDP REST server
based on [AuthzForce core](https://github.com/authzforce/core). This container packages the PDP as well as the CLI application that is part of the core
for easy testing. It can be deployed and used by other applications to provide external access policy controls based on specified
[policies](https://github.com/fabric-testbed/Authz/tree/master/policies).

## Principle of operation

This container exposes several mount points/volumes to externalize configuration of the app and policies. At startup it copies default config files into
the host filesystem using those mounts and starts up with a default configuration. In order to make it operational, several files need to be edited:
- conf/pdp.xml needs to be pointed to the correct XML policy file and root policy name
- conf/logback.xml can be modified to change the logging configuration
- conf/application.yml can be modified to add TLS support

By default the container exposes ports 8080 (plaintext) and 8443 (TLS, if configured) for requests.

## Configuring and running the container

1. Pick locations on host filesystem where configuration (`/conf`) and security policies (`/policies`) will reside
1. Start the container (note where in this example `/conf` and `/policies` are mapped to and adjust accordingly):
```
docker run -d \
  --user=$(id -u):$(id -g) \
  --name=pdp \
  --publish=8080:8080 \
  --publish=8443:8443 \
  --volume=$(pwd)/newconf:/conf \
  --volume=$(pwd)/newpolicies:/policies \
  fabrictestbed/pdp:latest
```
1. Check the logs from the container
```
$ docker logs pdp
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::       (v1.5.14.RELEASE)
2020-05-12 18:41:19.432  INFO 6 --- [           main] ationConfigEmbeddedWebApplicationContext : Refreshing org.springframework.boot.context.embedded.AnnotationConfigEmbeddedWebApplicationContext@6bf2d08e: startup date [Tue May 12 18:41:19 GMT 2020]; root of context hierarchy
2020-05-12 18:41:19.784  INFO 6 --- [           main] o.s.b.f.xml.XmlBeanDefinitionReader      : Loading XML bean definitions from URL [file:/conf/spring-beans.xml]
2020-05-12 18:41:20.037  INFO 6 --- [           main] o.s.b.f.xml.XmlBeanDefinitionReader      : Loading XML bean definitions from class path resource [META-INF/cxf/cxf.xml]
2020-05-12 18:41:20.053  INFO 6 --- [           main] o.s.b.f.s.DefaultListableBeanFactory     : Overriding bean definition for bean 'org.apache.cxf.bus.spring.BusWiringBeanFactoryPostProcessor' with a different definition: replacing [Root bean: class [org.apache.cxf.bus.spring.BusWiringBeanFactoryPostProcessor]; scope=; abstract=false; lazyInit=false; autowireMode=0; dependencyCheck=0; autowireCandidate=true; primary=false; factoryBeanName=null; factoryMethodName=null; initMethodName=null; destroyMethodName=null] with [Generic bean: class [org.apache.cxf.bus.spring.BusWiringBeanFactoryPostProcessor]; scope=; abstract=false; lazyInit=false; autowireMode=0; dependencyCheck=0; autowireCandidate=true; primary=false; factoryBeanName=null; factoryMethodName=null; initMethodName=null; destroyMethodName=null; defined in class path resource [META-INF/cxf/cxf.xml]]
2020-05-12 18:41:20.704  INFO 6 --- [           main] s.b.c.e.t.TomcatEmbeddedServletContainer : Tomcat initialized with port(s): 8080 (http)
2020-05-12 18:41:20.809  INFO 6 --- [ost-startStop-1] o.s.web.context.ContextLoader            : Root WebApplicationContext: initialization completed in 1382 ms
2020-05-12 18:41:21.066  INFO 6 --- [ost-startStop-1] o.s.b.w.servlet.ServletRegistrationBean  : Mapping servlet: 'dispatcherServlet' to [/]
2020-05-12 18:41:21.068  INFO 6 --- [ost-startStop-1] o.s.b.w.servlet.ServletRegistrationBean  : Mapping servlet: 'CXFServlet' to [/services/*]
2020-05-12 18:41:21.070  INFO 6 --- [ost-startStop-1] o.s.b.w.servlet.FilterRegistrationBean   : Mapping filter: 'characterEncodingFilter' to: [/*]
2020-05-12 18:41:21.071  INFO 6 --- [ost-startStop-1] o.s.b.w.servlet.FilterRegistrationBean   : Mapping filter: 'hiddenHttpMethodFilter' to: [/*]
2020-05-12 18:41:21.071  INFO 6 --- [ost-startStop-1] o.s.b.w.servlet.FilterRegistrationBean   : Mapping filter: 'httpPutFormContentFilter' to: [/*]
2020-05-12 18:41:21.071  INFO 6 --- [ost-startStop-1] o.s.b.w.servlet.FilterRegistrationBean   : Mapping filter: 'requestContextFilter' to: [/*]
2020-05-12 18:41:22.304  INFO 6 --- [           main] s.w.s.m.m.a.RequestMappingHandlerAdapter : Looking for @ControllerAdvice: org.springframework.boot.context.embedded.AnnotationConfigEmbeddedWebApplicationContext@6bf2d08e: startup date [Tue May 12 18:41:19 GMT 2020]; root of context hierarchy
2020-05-12 18:41:22.375  INFO 6 --- [           main] s.w.s.m.m.a.RequestMappingHandlerMapping : Mapped "{[/error],produces=[text/html]}" onto public org.springframework.web.servlet.ModelAndView org.springframework.boot.autoconfigure.web.BasicErrorController.errorHtml(javax.servlet.http.HttpServletRequest,javax.servlet.http.HttpServletResponse)
2020-05-12 18:41:22.376  INFO 6 --- [           main] s.w.s.m.m.a.RequestMappingHandlerMapping : Mapped "{[/error]}" onto public org.springframework.http.ResponseEntity<java.util.Map<java.lang.String, java.lang.Object>> org.springframework.boot.autoconfigure.web.BasicErrorController.error(javax.servlet.http.HttpServletRequest)
2020-05-12 18:41:22.408  INFO 6 --- [           main] o.s.w.s.handler.SimpleUrlHandlerMapping  : Mapped URL path [/webjars/**] onto handler of type [class org.springframework.web.servlet.resource.ResourceHttpRequestHandler]
2020-05-12 18:41:22.408  INFO 6 --- [           main] o.s.w.s.handler.SimpleUrlHandlerMapping  : Mapped URL path [/**] onto handler of type [class org.springframework.web.servlet.resource.ResourceHttpRequestHandler]
2020-05-12 18:41:22.443  INFO 6 --- [           main] o.s.w.s.handler.SimpleUrlHandlerMapping  : Mapped URL path [/**/favicon.ico] onto handler of type [class org.springframework.web.servlet.resource.ResourceHttpRequestHandler]
2020-05-12 18:41:22.575  INFO 6 --- [           main] o.s.j.e.a.AnnotationMBeanExporter        : Registering beans for JMX exposure on startup
2020-05-12 18:41:22.609  INFO 6 --- [           main] s.b.c.e.t.TomcatEmbeddedServletContainer : Tomcat started on port(s): 8080 (http)
```
1. If the conf directory is empty on first startup, it gets filled from inside the container with default configuration files, the container starts with a default simple ProjectPolicy
1. You can test the container by sending it a request as follows (the `ProjCreateDeleteRequest.xml` file is provided together with the `ProjectPolicy.xml` in `/policies` upon startup, be sure to provide the full path to it on host filesystem):
```
$ curl --include --header "Content-Type: application/xacml+xml" --data @newpolicies/ExampleProjRequest.xml http://localhost:8080/services/pdp | tidy -xml -i -
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                               Dload  Upload   Total   Spent    Left  Speed
100  2506  100   175  100  2331  13461   175k --:--:-- --:--:-- --:--:--  188k
line 8 column 1 - Warning: discarding unexpected plain text
1 warning, 0 errors were found!
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<Response xmlns="urn:oasis:names:tc:xacml:3.0:core:schema:wd-17">
<Result>
  <Decision>Permit</Decision>
</Result>
</Response>
```
1. You can then customize the container by placing a new policy file into the host-mapped `/policies` directory and updating `/conf/pdp.xml` to point to the policy file (`policyLocation` element) and the root policy elements (`rootPolicyRef` element):
```
<?xml version="1.0" encoding="UTF-8"?>
<pdp xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://authzforce.github.io/core/xmlns/pdp/7" version="7.1" maxVariableRefDepth="10" maxPolicyRefDepth="10"
	strictAttributeIssuerMatch="false">
	<!-- You may customize this PDP configuration except 'rootPolicyProvider' element. -->
	<policyProvider id="rootPolicyProvider" xsi:type="StaticPolicyProvider">
		<policyLocation>/policies/ProjectPolicy.xml</policyLocation>
	</policyProvider>
	<!-- Must match the Policy(Set)Id of one of the Policies/PolicySets provided by the 'policyProvider', the one with which the PDP starts the evaluation (root policy).  -->
	<rootPolicyRef>urn:fabric:authz:xacml:ProjectExample1</rootPolicyRef>
	<ioProcChain>
		<!-- XACML/XML processing chain. Replace requestPreproc value with "urn:ow2:authzforce:feature:pdp:request-preproc:xacml-xml:multiple:repeated-attribute-categories-lax" for Multiple Decision Profile
			support. -->
		<requestPreproc>urn:ow2:authzforce:feature:pdp:request-preproc:xacml-xml:default-lax</requestPreproc>
	</ioProcChain>
	<ioProcChain>
		<!-- XACML/JSON processing chain. -->
		<requestPreproc>urn:ow2:authzforce:feature:pdp:request-preproc:xacml-json:default-lax</requestPreproc>
		<resultPostproc>urn:ow2:authzforce:feature:pdp:result-postproc:xacml-json:default</resultPostproc>
	</ioProcChain>
</pdp>
```

## Using the in-built CLI tool

You can open a shell into the running container and run the CLI tool:
```
$ docker exec -ti pdp bash
```
From there navigate to `/opt/authzforce/bin` and you can execute the appropriate version of the CLI tool:
```
$  ./cli-15.1.0-app.jar -p /conf/pdp.xml /policies/ExampleProjRequest.xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Response xmlns="urn:oasis:names:tc:xacml:3.0:core:schema:wd-17">
    <Result>
        <Decision>Permit</Decision>
    </Result>
</Response>
```
This allows to easily test policies without using curl/REST.

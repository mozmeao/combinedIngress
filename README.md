# CombinedIngress

This is a really small little program that takes a few arguments, such as the name of the docker service, the port the service listens on, and a number of demo sites to expose to the world.

# Usage

Build/publish a docker container.  For local usage, this will work well:
`docker build . -t ci`  
 
 Then, run the container. (assuming you have an output dir, mkdir output), and the k8s service is named test.  You namespaces are demo1/demo2. Then you'll get these dns names, demo1.example.com, demo2.example.com pointing at these services.
 
 `docker run -v `PWD`/output:/output ci "test" "80" "example.org" "demo1" "demo2"`
 
 A quick diagram of the way this works.  We're being opinionated about a few things, like the route53 entries being all in the same domain.  And the k8s namespace and left most part of the dns entry being identical. The k8s namespace of the ingress is per service, as a way of making it possible to reuse this project.
                                                                               
                                                     K8s objects              
 Route53 entries                                                              
                          AWS Alb/k8s ingress        +-------------------+    
 +-------------------+    (created by this           |demo1 namespace    |    
 |demo1.example.com  |    project's yml)             |                   |    
 |                   |                               |test:80 k8s service|    
 +-------------------|   +-------------------+       --------------------+    
                     +---- k8s namespace:    --------+                        
 +-------------------+---- demo-shared-test  --------+                        
 |demo2.example.com  |   +-------------------+       --------------------+    
 |                   |                               |demo2 namespace    |    
 +-------------------+                               |                   |    
                                                     |test:80 k8s service|    
                                                     +-------------------+   
 
 
 # TODO
 
 * do a refactor to put the yaml in templates instead of building in code
 
# personal-cloud
personal-cloud (as a reference to Personal Coputer / PC) is a collection of How-To that we developed at April Software to run our software stack. We think it could benefit to others. 

We decided to run our own IT infrastructure based on the principle of being as less as possible dependent on commercial software or commercially supported open source software. 
There are pro and cons using commercial software or open source software. We believe in open source and to the power of the community. We think that it is the most sustainable approach and we believe in long term businesses.  

The open source ecosystem is very rich and provides everything you would need to build your own infrastructure. There are almost endless possibilities and picking up the different components that you would need to build you own infrastructure could be a challenging task.

We selected [Debian](https://www.debian.org/) as operating system. There are very good alternatives to Debian; which are eventually backed by commercial companies. Howver Debian fits with the principle of being as less as possible dependent on commercial software and commercially supported open source software. Even do they remain open source software, some other distributions are governed mainly by the companies that support them. On the other end, Debian is governed by the Debian community. Again there are pro and cons and we can debate it years. Our intention here is about sharing the knowledge we collected over the years operating the software stack we built.

We selected [GlusterFS](https://www.gluster.org/) for the storage for its simplicity and its relability. 

The first brick of the infrastructure is what we called a Personal Cluster (Here also as a reference to PC, the three being different abstraction layers). The Personal Cluster takes care of the VMs and their Storage in a high availability way. From there we deploy Kubernetes Clusters and cloud services.

Building a cluster requires you to have sevral computers available. The minimum is 2 and the more is the better. However the number of computers follows the rules given by GlusterFS. Depending on the number of replica you would like to keep, it should be a multiple of it. For instance, you could have a cluster or 2, 4, 6, x nodes storing 2 replicas or most probably 3, 6, 9, x storing 3 replicas (to avoid Split-Brains).

[Start by installing your first Personal Cluster to operate your first Personal Cloud](personal-cluster.md).
